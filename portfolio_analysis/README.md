# Wealth Management Final Coding Individual Assignment

### **Task**: To provide full risk and return analysis of the portfolio and make recommendations on rebalancing for an Ultra High Net Worth client, based in Palo Alto, CA. Your investor has the following assets:

| Ticker | Name | Current % allocation | Asset class | What it tracks? |
| --- | --- | --- | --- | --- |
| IXN | https://hedgefollow.com/stocks/IXN | 17.5% | Equity | seeks to track the investment results of an index composed of global equities in the technology sector |
| QQQ | https://hedgefollow.com/stocks/QQQ | 22.1% | Equity | Seeks to track the NASDAQ-100 Index that is made of 100 largest non-financial companies listed on NASDAQ |
| IEF | https://hedgefollow.com/stocks/IEF | 28.5% | Fixed Income | Seeks to tracks the investment results of an index composed of U.S. Treasury bonds with remaining maturities between seven and ten years |
| VNQ | https://hedgefollow.com/stocks/VNQ | 8.9% | Real Estate | Seeks to track the performance of the MSCI US Investable Market Real Estate 25/50 Index |
| GLD | https://hedgefollow.com/stocks/GLD | 23% | Commodities | seeks to track an index: LBMA London Gold Market Fixing Price PM Index. The GLD ETF provides physical exposure, so by buying it you actually own parts of all the underlying holdings |

### 1) Most Recent Returns for the each of the securities and the entire portfolio:

| Asset | IXN | QQQ | IEF | VNQ | GLD | Portfolio |
| --- | --- | --- | --- | --- | --- | --- |
| Monthly Return over 12 Months | 2.76% | 2.25% | -0.04% | 0.40% | 1.76% | 1.41% |
| Monthly Return over 18 Months | 3.26% | 3.02% | -0.22% | -0.08% | 1.29% | 1.46% |
| Monthly Return over 24 Months | 2.4% | 2.06% | -0.39% | -0.31% | 1.37% | 1.05% |
| 12 Months Return | 38.61% | 30.57% | -0.49% | 4.80% | 23.25% | 18.25% |
| 18 Months Return | 78.05% | 70.82% | -3.82% | -1.44% | 25.96% | 29.93% |
| 24 Months Return | 76.40% | 63.20% | -8.96% | -7.30% | 38.5% | 28.47% |

**Code for Expected returns of the individual securities (both monthly and over the period):**

```r
## expected monthly returns of the assets over 12 months
exp_returns_ixn <- mean(joined_monthly_returns$ixn[time_index:(time_index-11)])
exp_returns_qqq <- mean(joined_monthly_returns$qqq[time_index:(time_index-11)])
exp_returns_ief <- mean(joined_monthly_returns$ief[time_index:(time_index-11)])
exp_returns_vnq <- mean(joined_monthly_returns$vnq[time_index:(time_index-11)])
exp_returns_gld <- mean(joined_monthly_returns$gld[time_index:(time_index-11)])

## expected monthly returns of the assets over 18 months
exp_returns_ixn_18 <- mean(joined_monthly_returns$ixn[time_index:(time_index-17)])
exp_returns_qqq_18 <- mean(joined_monthly_returns$qqq[time_index:(time_index-17)])
exp_returns_ief_18 <- mean(joined_monthly_returns$ief[time_index:(time_index-17)])
exp_returns_vnq_18 <- mean(joined_monthly_returns$vnq[time_index:(time_index-17)])
exp_returns_gld_18 <- mean(joined_monthly_returns$gld[time_index:(time_index-17)])

## expected monthly returns of the assets over 24 months
exp_returns_ixn_24 <- mean(joined_monthly_returns$ixn[time_index:(time_index-23)])
exp_returns_qqq_24 <- mean(joined_monthly_returns$qqq[time_index:(time_index-23)])
exp_returns_ief_24 <- mean(joined_monthly_returns$ief[time_index:(time_index-23)])
exp_returns_vnq_24 <- mean(joined_monthly_returns$vnq[time_index:(time_index-23)])
exp_returns_gld_24 <- mean(joined_monthly_returns$gld[time_index:(time_index-23)])

## 12 Months assets Return
exp_returns_ixn_12mr <- ((1+exp_returns_ixn)^12) - 1
exp_returns_qqq_12mr <- ((1+exp_returns_qqq)^12) - 1
exp_returns_ief_12mr <- ((1+exp_returns_ief)^12) - 1
exp_returns_vnq_12mr <- ((1+exp_returns_vnq)^12) - 1
exp_returns_gld_12mr <- ((1+exp_returns_gld)^12) - 1

## 18 Months assets Return
exp_returns_ixn_18mr <- ((1+exp_returns_ixn_18)^18) - 1
exp_returns_qqq_18mr <- ((1+exp_returns_qqq_18)^18) - 1
exp_returns_ief_18mr <- ((1+exp_returns_ief_18)^18) - 1
exp_returns_vnq_18mr <- ((1+exp_returns_vnq_18)^18) - 1
exp_returns_gld_18mr <- ((1+exp_returns_gld_18)^18) - 1

## 24 Months assets Return
exp_returns_ixn_24mr <- ((1+exp_returns_ixn_24)^24) - 1
exp_returns_qqq_24mr <- ((1+exp_returns_qqq_24)^24) - 1
exp_returns_ief_24mr <- ((1+exp_returns_ief_24)^24) - 1
exp_returns_vnq_24mr <- ((1+exp_returns_vnq_24)^24) - 1
exp_returns_gld_24mr <- ((1+exp_returns_gld_24)^24) - 1
```

**Code for Expected Portfolio returns for 12, 18, and 24 Months (both monthly and over the period):**

```r
## creating portfolio returns

# assigning weightage (as per the original allocation)
ixn_w <- 0.175
qqq_w <- 0.221
ief_w <- 0.285
vnq_w <- 0.089
gld_w <- 0.23

# calculating monthly returns with weightage per asset
joined_monthly_returns <- as.data.frame(joined_monthly_returns) %>%
  mutate(portfolio = ixn_w * ixn +
           qqq_w * qqq +
           ief_w * ief +
           vnq_w * vnq +
           gld_w * gld)

# portfolio sigma (12 months)
port_sigma <- sd(joined_monthly_returns$portfolio[time_index:(time_index-11)])*sqrt(12)

## portfolio monthly expected returns (12 months)
port_expected <- mean(joined_monthly_returns$portfolio[time_index:(time_index-11)])

## portfolio monthly expected returns (18 months)
port_expected_18 <- mean(joined_monthly_returns$portfolio[time_index:(time_index-17)])

## portfolio monthly expected returns (24 months)
port_expected_24 <- mean(joined_monthly_returns$portfolio[time_index:(time_index-23)])

## portfolio 12 months return
port_expected_12mr <- ((1+port_expected)^12) - 1

## portfolio 18 months return
port_expected_18mr <- ((1+port_expected_18)^18) - 1

## portfolio 24 months return
port_expected_24mr <- ((1+port_expected_24)^24) - 1
```

### 2) Correlation among Assets:

Heat Map representing correlation among assets, VONE benchmark, and the Portfolio

![Untitled](Wealth%20Management%20Final%20Coding%20Individual%20Assignme%20aae42e21fd594bc7a551e007206a9588/Untitled.png)

Interesting correlations among the assets are:

1. **IXN and QQQ** have a correlation of **97.89%**, now this is interesting because IXN tracks the tech stocks and QQQ tracks top 100 non-financial large-cap companies. Such high correlation shows that most of the tech companies hold the position in top 100 large cap listed on NASDAQ. It will be really interesting to see how in the next 5-10 years, with the advancements in AI, which other tech companies join the club. 
2. **QQQ and IEF** have a correlation of **83.64%**, now this is unusual because bonds and equity market traditionally had an inverse relationship between them. Whenever both the markets have risen simultaneously, it indicated that there’s a bubble existing in the stock market and a market correction will happen sooner or later. However it’s not necessary that there’s a bubble; it could be because of the rising inflation as well. Further research will need to be done to be certain.
3. **GLD and QQQ** have a correlation of **8.25%**, which is kind of expected because gold is a safe investment and QQQ is tracking the top 100 non-financial large-caps. When the economy is booming, the stock market will be bullish too and stock market will be giving higher returns compared to safer investment option like gold and vice versa. And that’s why it’s great to have both in the portfolio for diversification.
4. **VNQ and QQQ** have a correlation of **90.05%**, its interesting to see this high correlation between the stock market and real estate because whenever the economy is growing and that’s when people have money to buy homes, make real estate investments, etc. Though there’s no direct causation effect between them. There are a lot of other factors affecting this.
5. **VNQ and GLD** have a correlation of **25.93%**, Gold and real estate market have a low correlation which is telling us that these 2 markets don’t rise and fall simultaneously. Keeping both in the portfolio will help to diversify the portfolio.

**Code to get the correlation among assets, VONE, and the portfolio:**

```r
## calculating correlation among assets in the portfolio
port_cor <- cor(joined_monthly_returns[time_index:(time_index-11), ])
```

### 3) Most recent 12M sigma (risk) for each of the securities (and for the entire portfolio)

| Asset | IXN | QQQ | IEF | VNQ | GLD | VONE | Portfolio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sigma | 0.2034621 | 0.1678823 | 0.0860061 | 0.2179634 | 0.1290978 | 0.1497312 | 0.1201649 |
| Sigma (%) | 20.35% | 16.79% | 8.60% | 21.80% | 12.91% | 14.97% | 12.02% |

![Untitled](Wealth%20Management%20Final%20Coding%20Individual%20Assignme%20aae42e21fd594bc7a551e007206a9588/Untitled%201.png)

**Code to get the sigma for each of the securities in the portfolio and the portfolio:**

```r
## Calculating the sigma (Internal Risk) for the assets in the portfolio and the benchmark VONE
sigma_ixn <- sd(joined_monthly_returns$ixn[time_index:(time_index-11)])*sqrt(12)
sigma_qqq <- sd(joined_monthly_returns$qqq[time_index:(time_index-11)])*sqrt(12)
sigma_ief <- sd(joined_monthly_returns$ief[time_index:(time_index-11)])*sqrt(12)
sigma_vnq <- sd(joined_monthly_returns$vnq[time_index:(time_index-11)])*sqrt(12)
sigma_gld <- sd(joined_monthly_returns$gld[time_index:(time_index-11)])*sqrt(12)
sigma_vone <- sd(joined_monthly_returns$vone[time_index:(time_index-11)])*sqrt(12)

## creating portfolio returns

# assigning weightage (as per the original allocation)
ixn_w <- 0.175
qqq_w <- 0.221
ief_w <- 0.285
vnq_w <- 0.089
gld_w <- 0.23

# calculating monthly returns with weightage per asset
joined_monthly_returns <- as.data.frame(joined_monthly_returns) %>%
  mutate(portfolio = ixn_w * ixn +
           qqq_w * qqq +
           ief_w * ief +
           vnq_w * vnq +
           gld_w * gld)

# portfolio sigma (12 months)
port_sigma <- sd(joined_monthly_returns$portfolio[time_index:(time_index-11)])*sqrt(12)
```

### 4) Rebalancing & Restructuring the securities in the portfolio

Based on the analysis done above, the best approach will be to **keep all the securities in the portfolio** because **each of the security in the portfolio represent a different kind of an asset**. Though the way the securities are currently distributed is not the ideal way to maximize returns. Diversification is important but we need to optimize the portfolio for which **we’ll have to rebalance the weightage assigned to the securities**. 

To achieve it, I assigned the minimum weight assigned per security to **2% (0.02)**

Maximum weightage assigned per security to **30% (0.03)**

And since the investor is from the Bay area, so the investor knows how the advancements in the AI today is growing at an exponential pace. There’s a new startup/ or a business idea coming up every other day. And **Microsoft** is a company that is leading this AI wave with OpenAI. It’s crucial for us to leverage this phase of growth in AI and have it as an individual stock added into our portfolio. **Introduction of MSFT into the portfolio will help us generate exponential returns in the future** as it’s very promising and MSFT is expected to soon go for a stock split. Such incidents and the timing is perfect to invest in MSFT and reap the benefits in the next 5-10 years.  

| Assets | Existing Weightage | New Weightage |
| --- | --- | --- |
| IXN | 17.5% | 2.51% |
| QQQ | 22.1% | 30% |
| IEF | 28.5% | 24.16% |
| VNQ | 8.9% | 2% |
| GLD | 23% | 30% |
|  |  |  |
| New Assets |  |  |
| MSFT | - | 11.33% |

### **5) The Returns, Risk and Sharpe Ratio have improved by rebalancing and restructuring the portfolio**

**Approach:** 

1. Used the Efficient frontier to calculate the optimized weightage for every asset in the existing portfolio. 
2. The returns and sigma improved without introducing any new assets. But it didn’t improve significantly.
3. So, To provide the best returns per unit risk to our investor, why not leverage the time we’re in and add **MSFT** to our portfolio because of its future potential and there’s a lot of scope for it to grow and give high returns.
4. So, added MSFT to the portfolio and we got **better returns** as shown in the table below, **Lower Sigma** compared to before, and much better **Sharpe Ratio**

| Annualized expected existing Portfolio Returns | 18.25% |
| --- | --- |
| Annualized expected new portfolio Returns (w MSFT) | 20.58% |
|  |  |
| Existing Sigma of portfolio (Internal Risk) | 12.02% |
| New Sigma of portfolio (w MSFT) | 10.76% |
|  |  |
| Existing Sharpe Ratio | 1.51 |
| New Sharpe Ratio (w MSFT) | 1.91 |

The visualized chart for the comparison of annualized expected returns, risk, and sharpe ratio are at the end of the document.

**Code used to calculate the new weightages for the assets with MSFT in the portfolio**

```r
## REBALANCING

enddate <- "2024-07-13"
startdate <- "2016-08-22"

# Define tickers
tickers <- c("IXN", "QQQ", "IEF", "VNQ", "GLD", "MSFT")

########################################
#
# Remaining code in between is same.
# Only showing the changes here.
# To refer to the entire code,
# checkout the R script
#
########################################

maxSharpe <- function(averet, rcov, shorts = F, wmax = 0.2, min.weight = 0.02) {
  optim.callback <- function(param, averet, rcov, reshigh, reslow, shorts) { 
    port.sol <- NULL
    try(port.sol <- portfolio.optim(x = averet, pm = param, covmat = rcov, reshigh = reshigh, reslow = reslow, shorts = shorts), silent = T)
    if (is.null(port.sol)) { ratio = 10^9 } else {
      m.return <- averet %*% port.sol$pw
      m.risk <- sqrt(as.vector(port.sol$pw %*% rcov %*% port.sol$pw))
      ratio <- m.return / m.risk
      assign("w", port.sol$pw, inherits = T)
    }
    return(ratio)
  }

### --> SKIPPED  

z <- maxSharpe(averet, rcov, shorts = F, wmax = 0.3)

print(z)
```

**Code used to calculate the updated returns, sigma, and Sharpe ratio for the new portfolio**

```r
## CREATING NEW PORTFOLIO WITH UPDATED WEIGHTAGES:

## creating new rebalanced and restructured portfolio returns (12 months)

# assigning new weightage
ixn_w_new <- 0.02513358 
qqq_w_new <- 0.3
ief_w_new <- 0.24157790 
vnq_w_new <- 0.02
gld_w_new <- 0.3
msft_w_new <- 0.11328852

# calculating monthly returns with weightage per asset
joined_monthly_returns_new <- as.data.frame(joined_monthly_returns) %>%
  mutate(portfolio = ixn_w_new * ixn +
           qqq_w_new * qqq +
           ief_w_new * ief +
           vnq_w_new * vnq +
           gld_w_new * gld + 
           msft_w_new * msft)

# New rebalanced and restructured  sigma (12 months)
port_sigma_new <- sd(joined_monthly_returns_new$portfolio[time_index:(time_index-11)])*sqrt(12)

# New rebalanced and restructured portfolio expected returns (12 months)
port_expected_new <- mean(joined_monthly_returns_new$portfolio[time_index:(time_index-11)])

print(port_sigma_new)
print(port_expected_new)

# new portfolio rebalanced annualized returns (12 months)
port_expected_new_12mr <- ((1+port_expected_new)^12) - 1

# New rebalanced and restructured portfolio expected returns (18 months)
port_expected_18_new <- mean(joined_monthly_returns_new$portfolio[time_index:(time_index-17)])

# New rebalanced and restructured portfolio expected returns (24 months)
port_expected_24_new <- mean(joined_monthly_returns_new$portfolio[time_index:(time_index-23)])

# New rebalanced and restructured portfolio sharpe ratio (12 months)
sharpe_ratio_port_new <- (((1+port_expected_new)^12)-1-riskfree)/port_sigma_new

## calculating correlation among assets in the new portfolio
port_cor_new <- cor(joined_monthly_returns_new[time_index:(time_index-11), ])
```

### 6) Efficient Frontier created for both Existing and new rebalanced and restructured portfolio:

| Assets | Sharpe Ratio |
| --- | --- |
| IXN | 1.89 |
| QQQ | 1.82 |
| GLD | 1.8 |
| MSFT | 1.92 |

**Efficient frontier for IXN, QQQ, and GLD (existing portfolio)**

![Untitled](Wealth%20Management%20Final%20Coding%20Individual%20Assignme%20aae42e21fd594bc7a551e007206a9588/Untitled%202.png)

As we can see in the picture above, Since gold has the lowest risk of all the 3 assets, so we can confidently say that the one below (towards RED color) is GLD. IXN and QQQ are ETFs pretty close which makes sense because they had a correlation of **97.8%** and that is the reason why they’re providing almost similar returns compared to the risk. IXN is the YELLOW one and QQQ is BLUE because IXN as we know it’s an ETF of global tech stocks so it’s more riskier and less diversified compared to QQQ which has top 100 non-financial large-cap companies.

The best place to invest based on the chart in between the stocks will be right above the belly button. A point where a tangent from (0,0) will meet the outside curve just above the belly button and that’ll be the point where there’ll be maximum expected returns per unit of risk. 

**Efficient frontier for IXN, QQQ, and MSFT (new portfolio)**

![ixn_qqq_msft_ef.png](Wealth%20Management%20Final%20Coding%20Individual%20Assignme%20aae42e21fd594bc7a551e007206a9588/ixn_qqq_msft_ef.png)

Here we can see that all the three assets are pretty close to each other compared to the Efficient Frontier (EF) curve for the old portfolio. 

It’s so because IXN is the YELLOW one and QQQ is BLUE just like before but MSFT is way more riskier and has the potential to generate better returns than GLD. That is why even the belly is forming way above the 2 ETF stocks and the best place to invest based on the chart in between the stocks will be right above the belly button. A point where a tangent from (0,0) will meet the outside curve just above the belly button and that’ll be the point where there’ll be maximum expected returns per unit of risk. 

And that point above the belly button will be close to ETFs but there’ll be some percentage of MSFT stock that’ll be there to buy so as to increase the returns. 

This plot helps us to visually see why adding MSFT into our portfolio increased our returns significantly and reduced risk because we kept GLD too and at a higher percentage to reduce risks. 

**Efficient Frontier plot for GLD, QQQ, and MSFT** 

![gld_qqq_msft.png](Wealth%20Management%20Final%20Coding%20Individual%20Assignme%20aae42e21fd594bc7a551e007206a9588/gld_qqq_msft.png)

As we can see in the plot that when we have GLD, QQQ, and MSFT, it’s best to invest right above the belly button that is getting formed at about 4% of risk. At that point, we’ll be able to have maximum returns with minimum profit. MSFT is the one at the top, GLD at the bottom with the least risk, and QQQ in the middle.

<aside>
💡 **NOTE:** Not pasting the code for calculating Efficient frontier and charts here because it’s the same template code with ticker names changed.

</aside>

**Old vs New Portfolio Performance Comparison (in terms of Expected Returns)**

![Untitled](Wealth%20Management%20Final%20Coding%20Individual%20Assignme%20aae42e21fd594bc7a551e007206a9588/Untitled%203.png)

**Old vs New Portfolio Performance Comparison (in terms of Internal Risk (Sigma))**

![Untitled](Wealth%20Management%20Final%20Coding%20Individual%20Assignme%20aae42e21fd594bc7a551e007206a9588/Untitled%204.png)

**Old vs New Portfolio Performance Comparison (in terms of Sharpe Ratio)**

![Untitled](Wealth%20Management%20Final%20Coding%20Individual%20Assignme%20aae42e21fd594bc7a551e007206a9588/Untitled%205.png)

**Comparison of all the assets in the portfolio based on Treynor Ratio**

![Untitled](Wealth%20Management%20Final%20Coding%20Individual%20Assignme%20aae42e21fd594bc7a551e007206a9588/Untitled%206.png)

As we can see in the above chart, that almost all the assets have a very low treynor ratio (ranging between -0.1 to 0.5) except GLD. 

Treynor Ratio is calculated with VONE as the benchmark Index and the reason GLD is so high is because gold doesn’t depend on the stock market performance. Prof Thomas mentioned that it doesn’t make sense to calculate Treynor Ratio for GLD because it’s not in the same market. I did this just to show all the assets in the portfolio and tell the reason why GLD has such a high Treynor Ratio. It’s value means that for 1 unit of external risk (market risk), GLD will give about 1.51 unit of returns.

**Trailing Error Visualized for every stock in the new portfolio**

![Untitled](Wealth%20Management%20Final%20Coding%20Individual%20Assignme%20aae42e21fd594bc7a551e007206a9588/Untitled%207.png)

As we can see here, as compared to VONE, GLD is expected to have high Standard deviation from the benchmark because it is not the right benchmark to compare returns of gold. VONE is Russel 1000 which is the benchmark used to track top 1000 companies. We can see that MSFT has a high Tracking error which means it’s more volatile i.e., more riskier than other stocks and QQQ which is an index tracking top 100 non-financial large-cap companies has the lowest tracking error because all the companies it’s tracking are in Russel 1000 list too. So there’s an overlap. Hence much lesser deviation.
