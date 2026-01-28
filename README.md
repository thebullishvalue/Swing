# SWING (स्विंग) - Portfolio Tracker

**A Hemrek Capital Product | v1.1.0**

Real-time ETF portfolio analytics with institutional-grade performance tracking and benchmark comparison.

## Features

### Dashboard Mode
- **Portfolio Snapshot**: Total value, gains, returns, today's return
- **Performance Analysis**: Top/bottom performers, gain distribution, treemap
- **Portfolio Details**: Complete holdings table with export

### Holdings Analytics (Institutional Grade)
- **Concentration Metrics**: HHI, Effective N, Gini Coefficient, Top 5/10 concentration
- **Performance Distribution**: Win rate, average/median returns, dispersion
- **Risk Contribution**: Weight-based risk decomposition
- **Concentration Curve**: Lorenz curve visualization
- **Treemap**: Visual weight/return distribution

### Analysis Mode (Bloomberg Terminal Grade)
- **Interactive Chart**: Portfolio vs Benchmark (NIFTY 50, NIFTY 500)
- **Timeframe Buttons**: 1W, 1M, 3M, 6M, YTD, 1Y, 2Y, 5Y, MAX
- **Risk-Adjusted Metrics**: 
  - Sharpe, Sortino, Calmar, Information Ratio, Treynor
  - Alpha, Beta, R-Squared, Correlation
  - VaR (95%, 99%), CVaR, Tracking Error
  - Up/Down Capture Ratios
- **Drawdown Analysis**: Interactive drawdown chart with max DD marker
- **Returns Distribution**: Histogram with VaR overlay
- **Rolling Analytics**: 63-day rolling Sharpe and Beta
- **Monthly Heatmap**: Year x Month returns matrix with YTD
- **Holding Attribution**: Individual contribution to portfolio return

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

## Hemrek Capital Design System

- Golden accent theme (#FFC300)
- Dark mode interface
- Consistent with NIRNAY, AARAMBH, ARTHAGATI, PRAGYAM
- Dynamic IST footer timestamp

## Version History

- v1.1.0: Institutional-grade analytics, benchmark comparison, advanced metrics
- v1.0.0: Initial release
