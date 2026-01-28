# SWING (स्विंग) - Portfolio Tracker

**A Hemrek Capital Product**

Real-time ETF portfolio analytics with performance tracking. Time series analysis and historical performance insights for Indian market ETFs.

## Features

- **Real-Time Prices**: Live price fetching from Yahoo Finance
- **Today's Return**: Daily P&L tracking with previous close comparison
- **Portfolio Snapshot**: Total value, gains, returns, concentration metrics
- **Performance Highlights**: Top/bottom performers by absolute and weighted returns
- **Analysis Mode**: Historical time series analysis with multiple periods
  - Period returns (1W, 1M, 3M, 6M, YTD, 1Y, 2Y)
  - Volatility and Sharpe Ratio
  - Max Drawdown analysis
  - Win Rate statistics
  - Daily returns distribution
  - Individual holding performance

## Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Requirements

- Python 3.10+
- streamlit
- pandas
- numpy
- plotly
- yfinance
- openpyxl

## Data Input

Place your portfolio data in `ETF Summary Report.xlsx` with columns:
- ASSET NAME
- SYMBOL (NSE ticker without .NS suffix)
- QUANTITY
- AVERAGE PRICE

## Version

v1.1.0 - Hemrek Capital Design System
