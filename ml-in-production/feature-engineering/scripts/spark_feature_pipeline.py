import os
import shutil
from pathlib import Path

from pyspark.sql import SparkSession, functions as F, Window
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, IntegerType, BooleanType,
)

BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
TOPIC = os.environ.get("KAFKA_TOPIC", "ecom-sessions")
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_OUTPUT = OUTPUT_DIR / "user_features.csv"

SCHEMA = StructType([
    StructField("timestamp", StringType()),
    StructField("event_id", StringType()),
    StructField("user_id", StringType()),
    StructField("event_type", StringType()),
    StructField("product_id", StringType()),
    StructField("product_category", StringType()),
    StructField("product_price", DoubleType()),
    StructField("quantity", IntegerType()),
    StructField("device", StringType()),
    StructField("os", StringType()),
    StructField("browser", StringType()),
    StructField("referral_source", StringType()),
    StructField("page_duration_sec", IntegerType()),
    StructField("is_member", BooleanType()),
    StructField("cart_total", DoubleType()),
    StructField("discount_pct", IntegerType()),
])


def mode_udf_col(df, group_col, target_col, alias):
    most_frequent = (
        df.groupBy(group_col, target_col)
        .count()
        .withColumn(
            "rn",
            F.row_number().over(
                Window.partitionBy(group_col).orderBy(F.desc("count"))
            ),
        )
        .filter(F.col("rn") == 1)
        .select(F.col(group_col), F.col(target_col).alias(alias))
    )
    return most_frequent


def main():
    spark = (
        SparkSession.builder
        .appName("EcomFeatureEngineering")
        .master("local[*]")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.13:4.1.2",
        )
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.driver.memory", "2g")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    print(f"Reading from Kafka topic '{TOPIC}' at {BROKER} ...")

    raw = (
        spark.read
        .format("kafka")
        .option("kafka.bootstrap.servers", BROKER)
        .option("subscribe", TOPIC)
        .option("startingOffsets", "earliest")
        .option("endingOffsets", "latest")
        .load()
    )

    events = (
        raw.selectExpr("CAST(value AS STRING) as json_str")
        .select(F.from_json(F.col("json_str"), SCHEMA).alias("data"))
        .select("data.*")
    )

    total_count = events.count()
    print(f"Total events consumed: {total_count:,}")

    event_types = [
        "page_view", "search", "product_click", "add_to_cart",
        "remove_from_cart", "purchase", "apply_coupon", "write_review",
    ]
    event_count_exprs = [
        F.sum(F.when(F.col("event_type") == et, 1).otherwise(0)).alias(f"{et}_count")
        for et in event_types
    ]

    features = events.groupBy("user_id").agg(
        F.count("*").alias("total_events"),
        *event_count_exprs,
        F.countDistinct("product_id").alias("unique_products"),
        F.countDistinct("product_category").alias("unique_categories"),
        F.round(F.avg("product_price"), 2).alias("avg_product_price"),
        F.round(F.max("product_price"), 2).alias("max_product_price"),
        F.round(F.avg("page_duration_sec"), 2).alias("avg_page_duration_sec"),
        F.sum("page_duration_sec").alias("total_page_duration_sec"),
        F.round(F.avg("quantity"), 2).alias("avg_quantity"),
        F.round(F.max("cart_total"), 2).alias("max_cart_total"),
        F.round(F.avg("cart_total"), 2).alias("avg_cart_total"),
        F.max(F.when(F.col("discount_pct") > 0, 1).otherwise(0)).alias("has_discount"),
        F.max("discount_pct").alias("max_discount_pct"),
        F.round(
            F.sum(F.col("is_member").cast("int")) / F.count("*"), 0
        ).alias("is_member"),
    )

    features = features.withColumn(
        "add_to_cart_ratio",
        F.round(F.col("add_to_cart_count") / F.col("total_events"), 4),
    ).withColumn(
        "search_to_cart_ratio",
        F.round(
            F.when(F.col("search_count") > 0, F.col("add_to_cart_count") / F.col("search_count"))
            .otherwise(0.0),
            4,
        ),
    ).withColumn(
        "did_purchase",
        F.when(F.col("purchase_count") > 0, 1).otherwise(0),
    )

    primary_device = mode_udf_col(events, "user_id", "device", "primary_device")
    primary_browser = mode_udf_col(events, "user_id", "browser", "primary_browser")
    primary_referral = mode_udf_col(events, "user_id", "referral_source", "primary_referral")
    primary_os = mode_udf_col(events, "user_id", "os", "primary_os")

    features = (
        features
        .join(primary_device, "user_id", "left")
        .join(primary_browser, "user_id", "left")
        .join(primary_referral, "user_id", "left")
        .join(primary_os, "user_id", "left")
    )

    features = features.withColumn("is_member", F.col("is_member").cast("int"))

    print(f"Engineered features for {features.count():,} users")
    features.printSchema()
    features.show(5, truncate=False)

    spark_tmp = str(OUTPUT_DIR / "_spark_tmp")
    features.coalesce(1).write.csv(spark_tmp, header=True, mode="overwrite")

    part_files = list(Path(spark_tmp).glob("part-*.csv"))
    if part_files:
        shutil.move(str(part_files[0]), str(CSV_OUTPUT))
    shutil.rmtree(spark_tmp, ignore_errors=True)

    print(f"\nFeatures written to {CSV_OUTPUT}")
    print(f"Rows: {features.count():,}")

    spark.stop()


if __name__ == "__main__":
    main()
