###########################################################################
###########################################################################
###########################################################################
#
#
# Reviewing the portfolio of an Ultra High Net Worth Individual
# And based on the analysis, rebalancing and diversifying his/her portfolio
#
#
###########################################################################
###########################################################################
###########################################################################


## importing all necessary libraries
library(stats)
library(dplyr)
library(scales)
library(tseries)
library(ggplot2)
library(reshape2)
library(quantmod)
library(quadprog)
library(data.table)


## get the monthly returns of existing assets in investor's portfolio
ixn <- monthlyReturn(getSymbols(Symbols = "IXN", auto.assign = F))
qqq <- monthlyReturn(getSymbols(Symbols = "QQQ", auto.assign = F))
ief <- monthlyReturn(getSymbols(Symbols = "IEF", auto.assign = F))
vnq <- monthlyReturn(getSymbols(Symbols = "VNQ", auto.assign = F))
gld <- monthlyReturn(getSymbols(Symbols = "GLD", auto.assign = F))
msft <- monthlyReturn(getSymbols(Symbols = "MSFT", auto.assign = F))

## creating a dataframe with monthly returns of all the assets in portfolio
joined_monthly_returns <- merge.xts(ixn,
                                    qqq,
                                    ief,
                                    vnq,
                                    gld,
                                    msft
                                    )


## adding a benchmark VONE for comparison
benchmark_returns <- monthlyReturn(getSymbols("VONE", auto.assign = F))


## joining the benchmark with the assets monthly returns dataframe
joined_monthly_returns <- merge.xts(joined_monthly_returns, benchmark_returns)


## renaming the column names for better readability
colnames(joined_monthly_returns) <- c("ixn","qqq","ief","vnq","gld","msft","vone")


## getting the total number of rows in our dataframe
time_index <- nrow(joined_monthly_returns)


## Calculating the sigma (Internal Risk) for the assets in the portfolio and the benchmark VONE
sigma_ixn <- sd(joined_monthly_returns$ixn[time_index:(time_index-11)])*sqrt(12)
sigma_qqq <- sd(joined_monthly_returns$qqq[time_index:(time_index-11)])*sqrt(12)
sigma_ief <- sd(joined_monthly_returns$ief[time_index:(time_index-11)])*sqrt(12)
sigma_vnq <- sd(joined_monthly_returns$vnq[time_index:(time_index-11)])*sqrt(12)
sigma_gld <- sd(joined_monthly_returns$gld[time_index:(time_index-11)])*sqrt(12)
sigma_msft <- sd(joined_monthly_returns$msft[time_index:(time_index-11)])*sqrt(12)
sigma_vone <- sd(joined_monthly_returns$vone[time_index:(time_index-11)])*sqrt(12)


## Calculating the Tracking error for the assets with comparison to the benchmark VONE
te_ixn <- sd(joined_monthly_returns$ixn[time_index:(time_index-11)]-joined_monthly_returns$vone[time_index:(time_index-11)])*sqrt(12)
te_qqq <- sd(joined_monthly_returns$qqq[time_index:(time_index-11)]-joined_monthly_returns$vone[time_index:(time_index-11)])*sqrt(12)
te_ief <- sd(joined_monthly_returns$ief[time_index:(time_index-11)]-joined_monthly_returns$vone[time_index:(time_index-11)])*sqrt(12)
te_vnq <- sd(joined_monthly_returns$vnq[time_index:(time_index-11)]-joined_monthly_returns$vone[time_index:(time_index-11)])*sqrt(12)
te_gld <- sd(joined_monthly_returns$gld[time_index:(time_index-11)]-joined_monthly_returns$vone[time_index:(time_index-11)])*sqrt(12)
te_msft <- sd(joined_monthly_returns$msft[time_index:(time_index-11)]-joined_monthly_returns$vone[time_index:(time_index-11)])*sqrt(12)


## Calculating Sharpe Ratio of individual assets
riskfree <- 0.0001


## expected monthly returns of the assets over 12 months
exp_returns_ixn <- mean(joined_monthly_returns$ixn[time_index:(time_index-11)])
exp_returns_qqq <- mean(joined_monthly_returns$qqq[time_index:(time_index-11)])
exp_returns_ief <- mean(joined_monthly_returns$ief[time_index:(time_index-11)])
exp_returns_vnq <- mean(joined_monthly_returns$vnq[time_index:(time_index-11)])
exp_returns_gld <- mean(joined_monthly_returns$gld[time_index:(time_index-11)])
exp_returns_msft <- mean(joined_monthly_returns$msft[time_index:(time_index-11)])


## expected monthly returns of the assets over 18 months
exp_returns_ixn_18 <- mean(joined_monthly_returns$ixn[time_index:(time_index-17)])
exp_returns_qqq_18 <- mean(joined_monthly_returns$qqq[time_index:(time_index-17)])
exp_returns_ief_18 <- mean(joined_monthly_returns$ief[time_index:(time_index-17)])
exp_returns_vnq_18 <- mean(joined_monthly_returns$vnq[time_index:(time_index-17)])
exp_returns_gld_18 <- mean(joined_monthly_returns$gld[time_index:(time_index-17)])
exp_returns_msft_18 <- mean(joined_monthly_returns$msft[time_index:(time_index-17)])


## expected monthly returns of the assets over 24 months
exp_returns_ixn_24 <- mean(joined_monthly_returns$ixn[time_index:(time_index-23)])
exp_returns_qqq_24 <- mean(joined_monthly_returns$qqq[time_index:(time_index-23)])
exp_returns_ief_24 <- mean(joined_monthly_returns$ief[time_index:(time_index-23)])
exp_returns_vnq_24 <- mean(joined_monthly_returns$vnq[time_index:(time_index-23)])
exp_returns_gld_24 <- mean(joined_monthly_returns$gld[time_index:(time_index-23)])
exp_returns_msft_24 <- mean(joined_monthly_returns$msft[time_index:(time_index-23)])


## 12 Months assets Return
exp_returns_ixn_12mr <- ((1+exp_returns_ixn)^12) - 1
exp_returns_qqq_12mr <- ((1+exp_returns_qqq)^12) - 1
exp_returns_ief_12mr <- ((1+exp_returns_ief)^12) - 1
exp_returns_vnq_12mr <- ((1+exp_returns_vnq)^12) - 1
exp_returns_gld_12mr <- ((1+exp_returns_gld)^12) - 1
exp_returns_msft_12mr <- ((1+exp_returns_msft)^12) - 1


## 18 Months assets Return
exp_returns_ixn_18mr <- ((1+exp_returns_ixn_18)^18) - 1
exp_returns_qqq_18mr <- ((1+exp_returns_qqq_18)^18) - 1
exp_returns_ief_18mr <- ((1+exp_returns_ief_18)^18) - 1
exp_returns_vnq_18mr <- ((1+exp_returns_vnq_18)^18) - 1
exp_returns_gld_18mr <- ((1+exp_returns_gld_18)^18) - 1
exp_returns_msft_18mr <- ((1+exp_returns_msft_18)^18) - 1


## 24 Months assets Return
exp_returns_ixn_24mr <- ((1+exp_returns_ixn_24)^24) - 1
exp_returns_qqq_24mr <- ((1+exp_returns_qqq_24)^24) - 1
exp_returns_ief_24mr <- ((1+exp_returns_ief_24)^24) - 1
exp_returns_vnq_24mr <- ((1+exp_returns_vnq_24)^24) - 1
exp_returns_gld_24mr <- ((1+exp_returns_gld_24)^24) - 1
exp_returns_msft_24mr <- ((1+exp_returns_msft_24)^24) - 1


## Calculating the Sharpe Ratio of every asset in the portfolio
sharpe_ratio_ixn <- (((1+exp_returns_ixn)^12)-1-riskfree)/sigma_ixn
sharpe_ratio_qqq <- (((1+exp_returns_qqq)^12)-1-riskfree)/sigma_qqq
sharpe_ratio_ief <- (((1+exp_returns_ief)^12)-1-riskfree)/sigma_ief
sharpe_ratio_vnq <- (((1+exp_returns_vnq)^12)-1-riskfree)/sigma_vnq
sharpe_ratio_gld <- (((1+exp_returns_gld)^12)-1-riskfree)/sigma_gld
sharpe_ratio_msft <- (((1+exp_returns_msft)^12)-1-riskfree)/sigma_msft


## creating portfolio returns

# assigning weightage (as per the original allocation)
ixn_w <- 0.175
qqq_w <- 0.221
ief_w <- 0.285
vnq_w <- 0.089
gld_w <- 0.23
msft_w <- 0


# calculating monthly returns with weightage per asset (existing portfolio)
joined_monthly_returns_ep <- as.data.frame(joined_monthly_returns) %>%
  mutate(portfolio = ixn_w * ixn +
           qqq_w * qqq +
           ief_w * ief +
           vnq_w * vnq +
           gld_w * gld + 
           msft_w * msft)

# portfolio sigma (12 months)
port_sigma <- sd(joined_monthly_returns_ep$portfolio[time_index:(time_index-11)])*sqrt(12)


## portfolio monthly expected returns (12 months)
port_expected <- mean(joined_monthly_returns_ep$portfolio[time_index:(time_index-11)])


## portfolio monthly expected returns (18 months)
port_expected_18 <- mean(joined_monthly_returns_ep$portfolio[time_index:(time_index-17)])


## portfolio monthly expected returns (24 months)
port_expected_24 <- mean(joined_monthly_returns_ep$portfolio[time_index:(time_index-23)])


## portfolio 12 months return
port_expected_12mr <- ((1+port_expected)^12) - 1


## portfolio 18 months return
port_expected_18mr <- ((1+port_expected_18)^18) - 1


## portfolio 24 months return
port_expected_24mr <- ((1+port_expected_24)^24) - 1


# portfolio sharpe ratio (12 months)
sharpe_ratio_port <- (((1+port_expected)^12)-1-riskfree)/port_sigma


## calculating correlation among assets in the portfolio
port_cor <- cor(joined_monthly_returns_ep[time_index:(time_index-11), ])
port_cor


# creating dataframe for last 12 months returns for the individual assets
last_12_months_returns <- joined_monthly_returns_ep[time_index:(time_index-11),]


## building CAPM to predict assets performance individually using Russel 1000
reg_ixn <- lm(ixn ~ vone, data=last_12_months_returns)
reg_qqq <- lm(qqq ~ vone, data=last_12_months_returns)
reg_ief <- lm(ief ~ vone, data=last_12_months_returns)
reg_vnq <- lm(vnq ~ vone, data=last_12_months_returns)
reg_gld <- lm(gld ~ vone, data=last_12_months_returns)
reg_msft <- lm(msft ~ vone, data=last_12_months_returns)


# Regression Model results for individual assets
summary(reg_ixn)
summary(reg_qqq)
summary(reg_ief)
summary(reg_vnq)
summary(reg_gld)
summary(reg_msft)

## Treynor Ratio of individual assets in the portfolio
trey_ixn <- (((1+exp_returns_ixn)^12)-1-riskfree)/reg_ixn$coefficients[2]
trey_qqq <- (((1+exp_returns_qqq)^12)-1-riskfree)/reg_qqq$coefficients[2]
trey_ief <- (((1+exp_returns_ief)^12)-1-riskfree)/reg_ief$coefficients[2]
trey_vnq <- (((1+exp_returns_vnq)^12)-1-riskfree)/reg_vnq$coefficients[2]
trey_gld <- (((1+exp_returns_gld)^12)-1-riskfree)/reg_gld$coefficients[2]
trey_msft <- (((1+exp_returns_msft)^12)-1-riskfree)/reg_msft$coefficients[2]


## REBALANCING


enddate <- "2024-07-13"
startdate <- "2016-08-22"

# Define tickers
tickers <- c("IXN", "QQQ", "IEF", "VNQ", "GLD", "MSFT")

# Fetch data for all tickers and align to common date range
all_data <- lapply(tickers, function(ticker) {
  tryCatch({
    data <- getSymbols(ticker, src = "yahoo", from = startdate, to = enddate, auto.assign = FALSE)
    Cl(data) # Use the adjusted closing price
  }, error = function(e) {
    warning(paste("Error fetching data for", ticker))
    return(NULL)
  })
})

# Convert list to data frame and find common date range
pricinglist <- do.call(merge, all_data)
pricinglist <- na.omit(pricinglist) # Remove rows with NA values

# Ensure the data frame has the correct number of rows
t <- nrow(pricinglist)
nstocks <- ncol(pricinglist)

# Forecasting the next price using a backpropagation training algorithm in a neural network. 
# An Autoregressive Model of fourth order AR4 was used.

newpricingdataset <- pricinglist

# Creating a dataset with monthly ROR for each day using continuous compounding
dailyROR <- as.data.frame(matrix(ncol = ncol(newpricingdataset), nrow = nrow(newpricingdataset) - 25))
colnames(dailyROR) <- colnames(pricinglist)
for (c in 1:ncol(newpricingdataset)) {
  for (r in 1:(nrow(newpricingdataset) - 25)) {
    dailyROR[r, c] <- log(as.numeric(newpricingdataset[(r + 25), c]) / as.numeric(newpricingdataset[r, c]))
  }
}
# The most current expected return for n+25 (n is today) is in the last row of the above dataset

# Calculating Expected(R) for all securities 
averet <- as.matrix(dailyROR[nrow(dailyROR), ], nrow = 1)
# Calculating covariance matrix
rcov <- cov(dailyROR[(nrow(dailyROR) - 125):(nrow(dailyROR)), ]) # 125 stands for 6 trading months
target.r <- 1 / 1000
# Using solver to get to optimal weights

effFrontier <- function(averet, rcov, nports, shorts, wmax, wmin) {
  mxret <- max(averet)
  mnret <- -mxret
  n.assets <- ncol(averet)
  reshigh <- rep(wmax, n.assets)
  reslow <- rep(wmin, n.assets)
  min.rets <- seq(mnret, mxret, length.out = nports)
  vol <- rep(NA, nports)
  ret <- rep(NA, nports)
  pw <- data.frame(matrix(ncol = nports, nrow = n.assets))
  for (i in 1:nports) {
    port.sol <- NULL
    try(port.sol <- portfolio.optim(x = averet, pm = min.rets[i], covmat = rcov, reshigh = reshigh, reslow = reslow, shorts = F), silent = T)
    if (!is.null(port.sol)) {
      vol[i] <- sqrt(as.vector(port.sol$pw %*% rcov %*% port.sol$pw))
      ret[i] <- averet %*% port.sol$pw
      pw[, i] <- port.sol$pw
    }
  }
  return(list(vol = vol, ret = ret, weights = pw))
}

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
  
  ef <- effFrontier(averet = averet, rcov = rcov, shorts = shorts, wmax = wmax, nports = 100, wmin = min.weight)
  n <- ncol(averet)
  reshigh <- rep(wmax, n)
  reslow <- rep(min.weight, n)
  
  max.sh <- which.max(ef$ret / ef$vol)
  
  if (is.na(ef$ret[max.sh - 1])) { lowerinterval <- ef$ret[max.sh] } else { lowerinterval <- ef$ret[max.sh - 1] }
  if (is.na(ef$ret[max.sh + 1])) { upperinterval <- ef$ret[max.sh] } else { upperinterval <- ef$ret[max.sh + 1] }
  
  w <- rep(0, ncol(averet))
  xmin <- optimize(f = optim.callback, interval = c(lowerinterval, upperinterval), 
                   averet = averet, rcov = rcov, reshigh = reshigh, reslow = reslow, shorts = shorts)
  return(w)
  return(xmin)
}

z <- maxSharpe(averet, rcov, shorts = F, wmax = 0.3)

print(z)


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

# new portfolio rebalanced annualized returns (18 months)
port_expected_new_18mr <- ((1+port_expected_new)^18) - 1

# new portfolio rebalanced annualized returns (24 months)
port_expected_new_24mr <- ((1+port_expected_new)^24) - 1

# New rebalanced and restructured portfolio expected returns (18 months)
port_expected_18_new <- mean(joined_monthly_returns_new$portfolio[time_index:(time_index-17)])

# New rebalanced and restructured portfolio expected returns (24 months)
port_expected_24_new <- mean(joined_monthly_returns_new$portfolio[time_index:(time_index-23)])

# New rebalanced and restructured portfolio sharpe ratio (12 months)
sharpe_ratio_port_new <- (((1+port_expected_new)^12)-1-riskfree)/port_sigma_new


## calculating correlation among assets in the new portfolio
port_cor_new <- cor(joined_monthly_returns_new[time_index:(time_index-11), ])



################################################################################
################################################################################
# 
# 
# VISUALIZATIONS
# 
# 
################################################################################
################################################################################


## BAR GRAPH comparing the portfolio returns. (old and new)
#  --------------------------------------------------------------

returns <- c(port_expected_12mr, port_expected_new_12mr)
colnames <- c("OLD_PORTFOLIO", "NEW_PORTFOLIO")

df <- data.frame(returns, colnames)

# Define the color palette
colors <- c("OLD_PORTFOLIO" = "lightblue", "NEW_PORTFOLIO" = "blue")

# Plot the returns with facets
ggplot(df, aes(x = colnames, y = returns, fill = colnames)) +
  geom_bar(stat = "identity") +
  scale_fill_manual(values = colors) +
  labs(title = "Comparison of New and Old Expected Annual Portfolio returns",
       x = "Portfolios",
       y = "Annualized Expected Returns") +
  theme_minimal() +
  theme(legend.position = "none")



## EFFICIENT FRONTINER

# GLD (1.8), IXN (1.89), and QQQ (1.82) have the highest Sharpe ratio in the existing portfolio. So, taking them to visualize the efficient frontier

# MSFT (1.92), IXN (1.89), and QQQ (1.82) have the highest Sharpe ratio in the new portfolio. So, taking them to visualize the efficient frontier

# efficient frontier 2 stocks
# load the data
ticker1_select <- "GLD"
ticker2_select <- "QQQ"
ticker3_select <- "MSFT"

mydf1 <- as.data.frame(monthlyReturn(getSymbols(ticker1_select, auto.assign=FALSE)))
mydf2 <- as.data.frame(monthlyReturn(getSymbols(ticker2_select, auto.assign=FALSE)))
mydf3 <- as.data.frame(monthlyReturn(getSymbols(ticker3_select, auto.assign=FALSE)))


combined_df <- cbind(mydf1[,1], mydf2[,1], mydf3[,1])

df <- as.data.frame(combined_df)
colnames(df) <- c("x","y", "z")
df$date = as.Date(rownames(mydf1))
# calculate the necessary values:
# I) expected returns for the two assets
er_x <- mean(df$x)
er_y <- mean(df$y)

# II) risk (standard deviation) as a risk measure
sd_x <- sd(df$x)
sd_y <- sd(df$y)

# III) covariance
cov_xy <- cov(df$x, df$y)

# create 1000 portfolio weights (omegas)
x_weights <- seq(from = 0, to = 1, length.out = 1000)

# create a data.table that contains the weights for the two assets
two_assets <- data.table(wx = x_weights,
                         wy = 1 - x_weights)

# calculate the expected returns and standard deviations for the 1000 possible portfolios
two_assets[, ':=' (er_p = wx * er_x + wy * er_y,
                   sd_p = sqrt(wx^2 * sd_x^2 +
                                 wy^2 * sd_y^2 +
                                 2 * wx * (1 - wx) * cov_xy))]
two_assets



# lastly plot the values
ggplot() +
  geom_point(data = two_assets, aes(x = sd_p, y = er_p, color = wx)) +
  geom_point(data = data.table(sd = c(sd_x, sd_y), mean = c(er_x, er_y)),
             aes(x = sd, y = mean), color = "red", size = 3, shape = 18) +
  # Miscellaneous Formatting
  theme_bw() + ggtitle("Possible Portfolios with Two Risky Assets - IXN & QQQ") +
  xlab("Volatility") + ylab("Expected Returns") +
  scale_y_continuous(label = percent, limits = c(0, max(two_assets$er_p) * 1.2)) +
  scale_x_continuous(label = percent, limits = c(0, max(two_assets$sd_p) * 1.2)) +
  scale_color_continuous(name = expression(omega[x]), labels = percent)



# Visualizing the efficient frontier for 3 stocks 
#  --------------------------------------------------------------

######################################################
### Three risky assets portfolio:
######################################################
# load the data

# calculate the necessary values:
# I) expected returns for the two assets
er_x <- mean(df$x)
er_y <- mean(df$y)
er_z <- mean(df$z)

# II) risk (standard deviation) as a risk measure
sd_x <- sd(df$x)
sd_y <- sd(df$y)
sd_z <- sd(df$z)

# III) covariance
cov_xy <- cov(df$x, df$y)
cov_xz <- cov(df$x, df$z)
cov_yz <- cov(df$y, df$z)

# create portfolio weights (omegas)
x_weights <- seq(from = 0, to = 1, length.out = 1000)

# create a data.table that contains the weights for the three assets
three_assets <- data.table(wx = rep(x_weights, each = length(x_weights)),
                           wy = rep(x_weights, length(x_weights)))

three_assets[, wz := 1 - wx - wy]


# calculate the expected returns and standard deviations for the 1000 possible portfolios
three_assets[, ':=' (er_p = wx * er_x + wy * er_y + wz * er_z,
                     sd_p = sqrt(wx^2 * sd_x^2 +
                                   wy^2 * sd_y^2 +
                                   wz^2 * sd_z^2 +
                                   2 * wx * wy * cov_xy +
                                   2 * wx * wz * cov_xz +
                                   2 * wy * wz * cov_yz))]

# take out cases where we have negative weights (shortselling)
three_assets <- three_assets[wx >= 0 & wy >= 0 & wz >= 0]
three_assets

# lastly plot the values
ggplot() +
  geom_point(data = three_assets, aes(x = sd_p, y = er_p, color = wx - wz)) +
  geom_point(data = data.table(sd = c(sd_x, sd_y, sd_z), mean = c(er_x, er_y, er_z)),
             aes(x = sd, y = mean), color = "red", size = 3, shape = 18) +
  # Miscellaneous Formatting
  theme_bw() + ggtitle("GLD, QQQ and MSFT") +
  xlab("Volatility (Risk)") + ylab("Expected Returns") +
  scale_y_continuous(label = percent, limits = c(0, max(three_assets$er_p) * 1.2)) +
  scale_x_continuous(label = percent, limits = c(0, max(three_assets$sd_p) * 1.2)) +
  scale_color_gradientn(colors = c("red", "blue", "yellow"),
                        name = expression(omega[x] - omega[z]), labels = percent)

