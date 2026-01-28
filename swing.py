# -*- coding: utf-8 -*-
"""
SWING (स्विंग) - Portfolio Tracker | A Hemrek Capital Product
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Real-time ETF portfolio analytics with performance tracking.
Time series analysis and historical performance insights.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO
from datetime import datetime, timedelta, timezone
import numpy as np
import locale
import yfinance as yf
import time

# --- Constants ---
VERSION = "v1.1.0"
PRODUCT_NAME = "Swing"
COMPANY = "Hemrek Capital"

# Streamlit page configuration
st.set_page_config(
    page_title="SWING | Portfolio Tracker",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

# --- Premium Professional CSS (Hemrek Capital Design System) ---
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        :root {
            --primary-color: #FFC300;
            --primary-rgb: 255, 195, 0;
            --background-color: #0F0F0F;
            --secondary-background-color: #1A1A1A;
            --bg-card: #1A1A1A;
            --bg-elevated: #2A2A2A;
            --text-primary: #EAEAEA;
            --text-secondary: #EAEAEA;
            --text-muted: #888888;
            --border-color: #2A2A2A;
            --border-light: #3A3A3A;
            
            --success-green: #10b981;
            --success-dark: #059669;
            --danger-red: #ef4444;
            --danger-dark: #dc2626;
            --warning-amber: #f59e0b;
            --info-cyan: #06b6d4;
            
            --neutral: #888888;
        }
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .main, [data-testid="stSidebar"] {
            background-color: var(--background-color);
            color: var(--text-primary);
        }
        
        .stApp > header {
            background-color: transparent;
        }
        
        #MainMenu {visibility: hidden;} footer {visibility: hidden;}
        
        .block-container {
            padding-top: 3.5rem;
            max-width: 90%; 
            padding-left: 2rem; 
            padding-right: 2rem;
        }
        
        /* Sidebar toggle button - always visible */
        [data-testid="collapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            background-color: var(--secondary-background-color) !important;
            border: 2px solid var(--primary-color) !important;
            border-radius: 8px !important;
            padding: 10px !important;
            margin: 12px !important;
            box-shadow: 0 0 15px rgba(var(--primary-rgb), 0.4) !important;
            z-index: 999999 !important;
            position: fixed !important;
            top: 14px !important;
            left: 14px !important;
            width: 40px !important;
            height: 40px !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        [data-testid="collapsedControl"]:hover {
            background-color: rgba(var(--primary-rgb), 0.2) !important;
            box-shadow: 0 0 20px rgba(var(--primary-rgb), 0.6) !important;
            transform: scale(1.05);
        }
        
        [data-testid="collapsedControl"] svg {
            stroke: var(--primary-color) !important;
            width: 20px !important;
            height: 20px !important;
        }
        
        [data-testid="stSidebar"] button[kind="header"] {
            background-color: transparent !important;
            border: none !important;
        }
        
        [data-testid="stSidebar"] button[kind="header"] svg {
            stroke: var(--primary-color) !important;
        }
        
        button[kind="header"] {
            z-index: 999999 !important;
        }
        
        [data-testid="stSidebar"] { 
            background: var(--secondary-background-color); 
            border-right: 1px solid var(--border-color); 
        }
        
        /* Premium Header Structure */
        .premium-header {
            background: var(--secondary-background-color);
            padding: 1.25rem 2rem;
            border-radius: 16px;
            margin-bottom: 1.5rem;
            box-shadow: 0 0 20px rgba(var(--primary-rgb), 0.1);
            border: 1px solid var(--border-color);
            position: relative;
            overflow: hidden;
            margin-top: 1rem;
        }
        
        .premium-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 50%, rgba(var(--primary-rgb),0.08) 0%, transparent 50%);
            pointer-events: none;
        }
        
        .premium-header h1 {
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.50px;
            position: relative;
        }
        
        .premium-header .tagline {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 0.25rem;
            font-weight: 400;
            position: relative;
        }
        
        /* Metric Card Styling */
        .metric-card {
            background-color: var(--bg-card);
            padding: 1.25rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0 0 15px rgba(var(--primary-rgb), 0.08);
            margin-bottom: 0.5rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            height: 100%;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.3);
            border-color: var(--border-light);
        }
        
        .metric-card h4 {
            color: var(--text-muted);
            font-size: 0.75rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .metric-card h2 {
            color: var(--text-primary);
            font-size: 1.75rem;
            font-weight: 700;
            margin: 0;
            line-height: 1;
        }
        
        .metric-card .sub-metric {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 0.5rem;
            font-weight: 500;
        }
        
        .metric-card.success h2 { color: var(--success-green); }
        .metric-card.danger h2 { color: var(--danger-red); }
        .metric-card.warning h2 { color: var(--warning-amber); }
        .metric-card.info h2 { color: var(--info-cyan); }
        .metric-card.neutral h2 { color: var(--neutral); }
        .metric-card.primary h2 { color: var(--primary-color); }

        /* Performance Card (for Highlights) */
        .performance-card {
            padding: 0.75rem; 
            border-radius: 6px;
            margin-bottom: 0.75rem; 
            background: var(--bg-elevated);
            border-left: 3px solid;
            transition: background 0.2s;
        }
        .performance-card:hover {
            background: var(--border-color);
        }
        
        .performance-card.positive { border-left-color: var(--success-green); }
        .performance-card.negative { border-left-color: var(--danger-red); }
        
        .performance-card .title {
            font-weight: 600;
            font-size: 1rem; 
            margin-bottom: 0.3rem;
            color: var(--text-primary);
        }
        
        .performance-card .stats {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem; 
            color: var(--text-primary);
            font-weight: 500;
            margin-bottom: 0.2rem;
        }

        .performance-section-header {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 5px;
        }

        .performance-subheader {
            font-size: 0.95rem;
            font-weight: 500;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }
        
        /* Table Styling */
        .table-container {
            width: 100%;
            overflow-x: auto;
            border-radius: 12px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            padding: 0;
        }
        
        table.table {
            width: 100%;
            table-layout: auto;
            border-collapse: collapse;
            color: var(--text-primary);
        }
        
        table.table th, table.table td {
            padding: 1rem 1.2rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        
        table.table th {
            font-weight: 600;
            color: var(--primary-color);
            background-color: var(--bg-elevated);
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.05em;
        }
        
        table.table td {
            font-size: 0.95rem;
        }
        
        table.table tr:hover {
            background: var(--bg-elevated);
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            background: transparent;
            padding: 0;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: var(--text-muted);
            border-bottom: 2px solid transparent;
            transition: color 0.3s, border-bottom 0.3s;
            background: transparent;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            color: var(--primary-color) !important;
            border-bottom: 2px solid var(--primary-color);
            background: transparent !important;
        }
        
        /* Utility classes */
        .positive { color: var(--success-green) !important; }
        .negative { color: var(--danger-red) !important; }
        .neutral { color: var(--text-primary) !important; }

        /* General Section Dividers/Headers */
        .section-header {
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border-color);
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0;
        }
        
        .section-subtitle {
            font-size: 0.95rem;
            color: var(--text-muted);
            margin: 0.25rem 0 0 0;
        }

        .section-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, var(--border-color) 50%, transparent 100%);
            margin: 1.5rem 0;
        }
        
        .sidebar-title { 
            font-size: 0.75rem; 
            font-weight: 700; 
            color: var(--primary-color); 
            text-transform: uppercase; 
            letter-spacing: 1px; 
            margin-bottom: 0.75rem; 
        }
        
        .info-box { 
            background: var(--secondary-background-color); 
            border: 1px solid var(--border-color); 
            padding: 1.25rem; 
            border-radius: 12px; 
            margin: 0.5rem 0; 
            box-shadow: 0 0 15px rgba(var(--primary-rgb), 0.08); 
        }
        .info-box h4 { color: var(--primary-color); margin: 0 0 0.5rem 0; font-size: 1rem; font-weight: 700; }
        .info-box p { color: var(--text-muted); margin: 0; font-size: 0.9rem; line-height: 1.6; }

        /* Buttons - Gold outline with glow on hover */
        .stButton>button {
            border: 2px solid var(--primary-color);
            background: transparent;
            color: var(--primary-color);
            font-weight: 700;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stButton>button:hover {
            box-shadow: 0 0 25px rgba(var(--primary-rgb), 0.6);
            background: var(--primary-color);
            color: #1A1A1A;
            transform: translateY(-2px);
        }
        
        .stButton>button:active {
            transform: translateY(0);
        }

        /* Download button styling */
        .stDownloadButton>button {
            border: 2px solid var(--primary-color);
            background: transparent;
            color: var(--primary-color);
            font-weight: 700;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stDownloadButton>button:hover {
            box-shadow: 0 0 25px rgba(var(--primary-rgb), 0.6);
            background: var(--primary-color);
            color: #1A1A1A;
            transform: translateY(-2px);
        }
        
        .stPlotlyChart {
            border-radius: 12px;
            background-color: var(--secondary-background-color);
            padding: 10px;
            border: 1px solid var(--border-color);
            box-shadow: 0 0 25px rgba(var(--primary-rgb), 0.1);
        }
        
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: var(--background-color); }
        ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--border-light); }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Function to fetch current prices from yfinance
@st.cache_data(ttl=300, show_spinner="Fetching real-time prices...")  # 5 min cache
def fetch_current_prices(symbols):
    """
    Fetches the latest closing price for a list of symbols with the .NS suffix.
    Returns a dictionary of {original_symbol: price}.
    
    Uses the same proven approach as returns.py:
    - Daily data (no intraday interval) to avoid rate limits
    - Single bulk download for all tickers
    - 5-day period to handle weekends/holidays
    """
    if not symbols:
        return {}

    # Add .NS suffix to symbols
    tickers_with_suffix = [f"{s}.NS" for s in symbols if s and isinstance(s, str)]
    
    prices = {}
    
    try:
        # Fetch daily data for last 5 days (handles weekends/holidays)
        # NO interval parameter = daily data = less rate limiting
        data = yf.download(
            tickers=tickers_with_suffix,
            period="5d",
            progress=False,
            auto_adjust=False
        )
        
        if data.empty:
            st.warning("yfinance returned empty data.")
            return {s: np.nan for s in symbols}
        
        # Get Close prices
        try:
            close_prices = data['Close']
        except KeyError:
            st.warning("No 'Close' column in fetched data.")
            return {s: np.nan for s in symbols}
        
        if close_prices.empty:
            return {s: np.nan for s in symbols}
        
        # Single ticker case: close_prices is a Series
        if len(tickers_with_suffix) == 1:
            ticker = tickers_with_suffix[0]
            original = ticker.replace('.NS', '')
            last_price = close_prices.dropna().iloc[-1] if not close_prices.dropna().empty else np.nan
            prices[original] = float(last_price) if not pd.isna(last_price) else np.nan
        
        # Multiple tickers case: close_prices is a DataFrame
        else:
            # Get last row (most recent date)
            latest_prices = close_prices.iloc[-1]
            
            for ticker in tickers_with_suffix:
                original = ticker.replace('.NS', '')
                try:
                    price = latest_prices[ticker]
                    prices[original] = float(price) if not pd.isna(price) else np.nan
                except (KeyError, TypeError):
                    prices[original] = np.nan
                    
    except Exception as e:
        st.error(f"Error fetching data from yfinance: {e}")
        return {s: np.nan for s in symbols}
    
    # Report any failures
    failed = [s for s in symbols if s in prices and pd.isna(prices.get(s))]
    if failed:
        st.warning(f"⚠️ Could not fetch prices for: {', '.join(failed[:5])}{'...' if len(failed) > 5 else ''}")
    
    return prices
    

# Function to load data
@st.cache_data
def load_data():
    file_path = "ETF Summary Report.xlsx"
    try:
        df = pd.read_excel(file_path)
        df = df.dropna(how='all')
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error(f"File '{file_path}' not found. Please upload the data file.")
        return None

# Function to fetch previous day close prices for Today Return calculation
@st.cache_data(ttl=300)
def fetch_previous_close(symbols):
    """Fetch previous trading day close prices for calculating today return."""
    if not symbols:
        return {}
    
    prices = {}
    tickers_with_suffix = [f"{s}.NS" for s in symbols]
    
    try:
        # Fetch 5 days of data to ensure we get previous close
        data = yf.download(
            tickers=tickers_with_suffix,
            period='5d',
            interval='1d',
            progress=False,
            threads=True
        )
        
        if data.empty:
            return {s: np.nan for s in symbols}
        
        close_prices = data['Close']
        
        # Single ticker case
        if len(tickers_with_suffix) == 1:
            ticker = tickers_with_suffix[0]
            original = ticker.replace('.NS', '')
            if len(close_prices.dropna()) >= 2:
                prev_close = close_prices.dropna().iloc[-2]  # Second to last
                prices[original] = float(prev_close)
            else:
                prices[original] = np.nan
        else:
            # Multiple tickers - get second to last row
            if len(close_prices) >= 2:
                prev_prices = close_prices.iloc[-2]
                for ticker in tickers_with_suffix:
                    original = ticker.replace('.NS', '')
                    try:
                        price = prev_prices[ticker]
                        prices[original] = float(price) if not pd.isna(price) else np.nan
                    except (KeyError, TypeError):
                        prices[original] = np.nan
            else:
                return {s: np.nan for s in symbols}
                
    except Exception as e:
        return {s: np.nan for s in symbols}
    
    return prices

# Function to calculate metrics
def calculate_metrics(df):
    df = df.copy()
    
    # 1. Fetch current prices
    symbols = df['SYMBOL'].tolist()
    price_map = fetch_current_prices(symbols)
    
    # 2. Fetch previous close for today's return
    prev_close_map = fetch_previous_close(symbols)
    
    # 3. Update CURRENT PRICE column using fetched data
    df['FETCHED PRICE'] = df['SYMBOL'].map(price_map)
    df['CURRENT PRICE'] = df['FETCHED PRICE'].fillna(df.get('CURRENT PRICE', df['AVERAGE PRICE']))
    
    # 4. Add previous close for today's return calculation
    df['PREV CLOSE'] = df['SYMBOL'].map(prev_close_map)
    
    # Check for critical missing data after fetch
    if df['CURRENT PRICE'].isnull().any():
        st.warning("⚠️ Some current prices could not be fetched. Using Average Price for calculation.")
    
    # 5. Perform calculations using the updated 'CURRENT PRICE'
    df['INVESTED'] = df['QUANTITY'] * df['AVERAGE PRICE']
    df['CURR. VALUE'] = df['QUANTITY'] * df['CURRENT PRICE']
    df['GAIN'] = df['CURR. VALUE'] - df['INVESTED']
    
    # Calculate today's change per holding
    df['TODAY CHANGE'] = np.where(
        df['PREV CLOSE'].notna(),
        (df['CURRENT PRICE'] - df['PREV CLOSE']) * df['QUANTITY'],
        0
    )
    df['TODAY %'] = np.where(
        (df['PREV CLOSE'].notna()) & (df['PREV CLOSE'] != 0),
        (df['CURRENT PRICE'] - df['PREV CLOSE']) / df['PREV CLOSE'] * 100,
        0
    )
    
    # Avoid division by zero
    df['GAIN %'] = np.where(df['INVESTED'] != 0, df['GAIN'] / df['INVESTED'] * 100, 0)
    
    total_curr_value = df['CURR. VALUE'].sum()
    df['WT'] = np.where(total_curr_value != 0, df['CURR. VALUE'] / total_curr_value * 100, 0)
    df['WEIGHTED RETURN %'] = df['GAIN %'] * df['WT'] / 100
    
    # Calculate today's portfolio return
    today_change_total = df['TODAY CHANGE'].sum()
    prev_portfolio_value = total_curr_value - today_change_total
    today_return_pct = (today_change_total / prev_portfolio_value * 100) if prev_portfolio_value != 0 else 0

    metrics = {
        'Total Current Value': total_curr_value,
        'Total Invested': df['INVESTED'].sum(),
        'Total Gain': df['GAIN'].sum(),
        'Portfolio Return %': np.where(df['INVESTED'].sum() != 0, df['GAIN'].sum() / df['INVESTED'].sum() * 100, 0),
        'Today Change': today_change_total,
        'Today Return %': today_return_pct,
        'Top 5 Concentration': df['WT'].nlargest(5).sum(),
        'Number of Holdings': len(df)
    }
    return df, metrics

# Function to format currency (Indian Rupee with Indian comma style)
def format_currency(value):
    """
    Formats a number in Indian numbering system (lakhs, crores).
    Example: 6797258.49 -> Rs 67,97,258.49
    """
    value = float(value)
    negative = value < 0
    value = abs(value)
    
    # Split into integer and decimal parts
    integer_part = int(value)
    decimal_part = value - integer_part
    
    # Convert integer to string
    int_str = str(integer_part)
    
    # Indian numbering: first group of 3 from right, then groups of 2
    if len(int_str) <= 3:
        formatted = int_str
    else:
        # Last 3 digits
        result = int_str[-3:]
        # Remaining digits, grouped by 2 from right to left
        remaining = int_str[:-3]
        while len(remaining) > 2:
            result = remaining[-2:] + ',' + result
            remaining = remaining[:-2]
        if remaining:
            result = remaining + ',' + result
        formatted = result
    
    # Add decimal places (always show 2 decimal places)
    formatted += f"{decimal_part:.2f}"[1:]
    
    formatted = f"{'-' if negative else ''}₹{formatted}"
    return formatted


# Function to create downloadable Excel
def to_excel(df):
    output = BytesIO()
    # Drop calculated columns that may cause issues or are redundant for a base export
    export_df = df.drop(columns=['INVESTED', 'CURR. VALUE', 'GAIN', 'GAIN %', 'WT', 'WEIGHTED RETURN %', 'FETCHED PRICE'], errors='ignore')
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        export_df.to_excel(writer, index=False, sheet_name='Portfolio')
    return output.getvalue()

# Main app
def main():
    # --- Sidebar Controls (Nirnay-style) ---
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
            <div style="font-size: 1.75rem; font-weight: 800; color: #FFC300;">SWING</div>
            <div style="color: #888888; font-size: 0.75rem; margin-top: 0.25rem;">स्विंग | Portfolio Tracker</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-title">🔄 Data Controls</div>', unsafe_allow_html=True)
        
        # Clear cache button (forces fresh fetch on next load)
        if st.button("REFRESH PRICES", help="Clear cached prices and fetch fresh data"):
            st.cache_data.clear()
            st.toast("Price cache cleared!", icon="🔄")
            st.rerun()
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-title">📊 View Mode</div>', unsafe_allow_html=True)
        view_mode = st.radio(
            "Select View",
            ["📈 Dashboard", "📉 Analysis Mode"],
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='info-box'>
            <p style='font-size: 0.8rem; margin: 0; color: var(--text-muted); line-height: 1.5;'>
                <strong>Version:</strong> {VERSION}<br>
                <strong>Data:</strong> Yahoo Finance<br>
                <strong>Refresh:</strong> Every 5 minutes
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Header - Using the premium-header structure
    st.markdown(f"""
        <div class="premium-header">
            <h1>SWING : Portfolio Tracker</h1>
            <div class="tagline">Real-Time ETF Analytics & Performance Insights</div>
        </div>
    """, unsafe_allow_html=True)

    # Load data
    df = load_data()
    if df is None:
        return

    # Verify required columns
    required_columns = ['ASSET NAME', 'SYMBOL', 'QUANTITY', 'AVERAGE PRICE']
    if not all(col in df.columns for col in required_columns):
        st.error(f"Excel file must contain: {', '.join(required_columns)}. The 'CURRENT PRICE' column is now automatically fetched.")
        return

    # Calculate metrics
    df, metrics = calculate_metrics(df)

    # Portfolio Snapshot Section
    st.markdown("""
        <div class='section'>
            <div class='section-header'>
                <h3 class='section-title'>Portfolio Snapshot</h3>
                <p class='section-subtitle'>Overview of your investment performance (Prices are near real-time)</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics in 4 columns (Holdings moved to dedicated tab)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class='metric-card primary'>
                <h4>Total Portfolio Value</h4>
                <h2 style='color: var(--primary-color);'>{format_currency(metrics['Total Current Value'])}</h2>
                <div class='sub-metric'>Invested: {format_currency(metrics['Total Invested'])}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        gain_class = 'success' if metrics['Total Gain'] >= 0 else 'danger'
        st.markdown(f"""
            <div class='metric-card {gain_class}'>
                <h4>Absolute Gain/Loss</h4>
                <h2 style='color: var(--{gain_class}-green);'>
                    {format_currency(metrics['Total Gain'])}
                </h2>
                <div class='sub-metric'>Since inception</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        return_class = 'success' if metrics['Portfolio Return %'] >= 0 else 'danger'
        st.markdown(f"""
            <div class='metric-card {return_class}'>
                <h4>Total Return</h4>
                <h2 style='color: var(--{return_class}-green);'>
                    {metrics['Portfolio Return %']:.2f}%
                </h2>
                <div class='sub-metric'>Portfolio XIRR equivalent</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        today_class = 'success' if metrics['Today Return %'] >= 0 else 'danger'
        today_sign = '+' if metrics['Today Change'] >= 0 else ''
        st.markdown(f"""
            <div class='metric-card {today_class}'>
                <h4>Today's Return</h4>
                <h2 style='color: var(--{today_class}-green);'>
                    {today_sign}{metrics['Today Return %']:.2f}%
                </h2>
                <div class='sub-metric'>{today_sign}{format_currency(metrics['Today Change'])}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # =========================================================================
    # DASHBOARD VIEW (Default)
    # =========================================================================
    if view_mode == "📈 Dashboard":
        # Tabs for detailed views
        tab1, tab2, tab3 = st.tabs(["**📊 Performance Analysis**", "**📋 Portfolio Details**", "**🎯 Holdings Analytics**"])

        with tab1:
            # Performance Highlights
            st.markdown("""
                <div class='section'>
                    <div class='section-header'>
                        <h3 class='section-title'>Performance Highlights</h3>
                        <p class='section-subtitle'>Top and bottom performing assets in your portfolio</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Side-by-side layout for Absolute Gain/Loss % and Weighted Return %
            col_metrics1, col_metrics2 = st.columns(2)

            # Section 1: Absolute Gain/Loss %
            with col_metrics1:
                st.markdown("<h3 class='performance-section-header'>Absolute Gain/Loss %</h3>", unsafe_allow_html=True)
                col_out1, col_under1 = st.columns(2)

                with col_out1:
                    st.markdown("<h4 class='performance-subheader'>Out-Performers</h4>", unsafe_allow_html=True)
                    top_performers_gain = df.nlargest(3, 'GAIN %')
                    for _, row in top_performers_gain.iterrows():
                        gain_color = 'success-green' if row['GAIN %'] >= 0 else 'danger-red'
                        weighted_color = 'success-green' if row['WEIGHTED RETURN %'] >= 0 else 'danger-red'
                        st.markdown(f"""
                            <div class='performance-card positive'>
                                <div class='title'>{row['SYMBOL']}</div>
                                <div class='stats'>
                                    <span>Gain/Loss</span>
                                    <span style='color: var(--{gain_color});'>{row['GAIN %']:.2f}%</span>
                                </div>
                                <div class='stats'>
                                    <span>Weighted Return</span>
                                    <span style='color: var(--{weighted_color});'>{row['WEIGHTED RETURN %']:.2f}%</span>
                                </div>
                                <div class='stats'>
                                    <span>Current Price</span>
                                    <span style='color: var(--text-primary);'>{format_currency(row['CURRENT PRICE'])}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                with col_under1:
                    st.markdown("<h4 class='performance-subheader'>Under-Performers</h4>", unsafe_allow_html=True)
                    bottom_performers_gain = df.nsmallest(3, 'GAIN %')
                    for _, row in bottom_performers_gain.iterrows():
                        gain_color = 'success-green' if row['GAIN %'] >= 0 else 'danger-red'
                        weighted_color = 'success-green' if row['WEIGHTED RETURN %'] >= 0 else 'danger-red'
                        card_class = "positive" if row['GAIN %'] >= 0 else "negative"
                        st.markdown(f"""
                            <div class='performance-card {card_class}'>
                                <div class='title'>{row['SYMBOL']}</div>
                                <div class='stats'>
                                    <span>Gain/Loss</span>
                                    <span style='color: var(--{gain_color});'>{row['GAIN %']:.2f}%</span>
                                </div>
                                <div class='stats'>
                                    <span>Weighted Return</span>
                                    <span style='color: var(--{weighted_color});'>{row['WEIGHTED RETURN %']:.2f}%</span>
                                </div>
                                <div class='stats'>
                                    <span>Current Price</span>
                                    <span style='color: var(--text-primary);'>{format_currency(row['CURRENT PRICE'])}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

            # Section 2: Weighted Return %
            with col_metrics2:
                st.markdown("<h3 class='performance-section-header'>Weighted Return %</h3>", unsafe_allow_html=True)
                col_out2, col_under2 = st.columns(2)

                with col_out2:
                    st.markdown("<h4 class='performance-subheader'>Out-Performers</h4>", unsafe_allow_html=True)
                    top_performers_weighted = df.nlargest(3, 'WEIGHTED RETURN %')
                    for _, row in top_performers_weighted.iterrows():
                        gain_color = 'success-green' if row['GAIN %'] >= 0 else 'danger-red'
                        weighted_color = 'success-green' if row['WEIGHTED RETURN %'] >= 0 else 'danger-red'
                        st.markdown(f"""
                            <div class='performance-card positive'>
                                <div class='title'>{row['SYMBOL']}</div>
                                <div class='stats'>
                                    <span>Gain/Loss</span>
                                    <span style='color: var(--{gain_color});'>{row['GAIN %']:.2f}%</span>
                                </div>
                                <div class='stats'>
                                    <span>Weighted Return</span>
                                    <span style='color: var(--{weighted_color});'>{row['WEIGHTED RETURN %']:.2f}%</span>
                                </div>
                                <div class='stats'>
                                    <span>Current Price</span>
                                    <span style='color: var(--text-primary);'>{format_currency(row['CURRENT PRICE'])}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                with col_under2:
                    st.markdown("<h4 class='performance-subheader'>Under-Performers</h4>", unsafe_allow_html=True)
                    bottom_performers_weighted = df.nsmallest(3, 'WEIGHTED RETURN %')
                    for _, row in bottom_performers_weighted.iterrows():
                        gain_color = 'success-green' if row['GAIN %'] >= 0 else 'danger-red'
                        weighted_color = 'success-green' if row['WEIGHTED RETURN %'] >= 0 else 'danger-red'
                        card_class = "positive" if row['WEIGHTED RETURN %'] >= 0 else "negative"
                        st.markdown(f"""
                            <div class='performance-card {card_class}'>
                                <div class='title'>{row['SYMBOL']}</div>
                                <div class='stats'>
                                    <span>Gain/Loss</span>
                                    <span style='color: var(--{gain_color});'>{row['GAIN %']:.2f}%</span>
                                </div>
                                <div class='stats'>
                                    <span>Weighted Return</span>
                                    <span style='color: var(--{weighted_color});'>{row['WEIGHTED RETURN %']:.2f}%</span>
                                </div>
                                <div class='stats'>
                                    <span>Current Price</span>
                                    <span style='color: var(--text-primary);'>{format_currency(row['CURRENT PRICE'])}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

            # Gain/Loss Distribution Histogram
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown("""
                <div class='section'>
                    <div class='section-header'>
                        <h3 class='section-title'>Gain/Loss Distribution</h3>
                        <p class='section-subtitle'>Performance across all holdings by weight rank</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Sort by weight (WT) in descending order and assign ranks
            sorted_df = df.sort_values('WT', ascending=False).reset_index(drop=True)
            sorted_df['Weight Rank'] = sorted_df.index + 1  # 1-based ranking
            
            # Create bar chart
            fig_gain = go.Figure()
            
            # Calculate bar width based on number of holdings for better aesthetics
            num_holdings = len(sorted_df)
            bar_width = min(0.8, 15 / num_holdings) if num_holdings > 0 else 0.8
            
            # Add Gain/Loss % bars with values on top
            fig_gain.add_trace(go.Bar(
                x=sorted_df['SYMBOL'],
                y=sorted_df['GAIN %'],
                name='Gain/Loss %',
                marker_color=['#10b981' if x >= 0 else '#ef4444' for x in sorted_df['GAIN %']],
                text=[f"{x:.2f}%" for x in sorted_df['GAIN %']],
                textposition='outside',
                textfont=dict(color='#EAEAEA', size=12),
                width=bar_width
            ))
            
            # Dynamic scaling for y-axis with extra padding for outside labels
            gain_min = sorted_df['GAIN %'].min()
            gain_max = sorted_df['GAIN %'].max()
            padding = max(abs(gain_min), abs(gain_max)) * 0.1
            extra_label_space = (gain_max - gain_min) * 0.1 if gain_max > 0 else 0
            y_range = [gain_min - padding, gain_max + padding + extra_label_space]
            
            fig_gain.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#EAEAEA"),
                margin=dict(l=0, r=0, t=20, b=0),
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)', 
                    title='Symbol (Ordered by Weight Rank)',
                    tickangle=45,
                    showgrid=False
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)', 
                    title='Gain/Loss (%)',
                    range=y_range
                ),
                showlegend=False,
                height=500,
                bargap=0.15
            )
            st.plotly_chart(fig_gain, width='stretch')

            # Portfolio Composition Treemap
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown("""
                <div class='section'>
                    <div class='section-header'>
                        <h3 class='section-title'>Portfolio Composition</h3>
                        <p class='section-subtitle'>Asset allocation by current value</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Dynamic color scale logic
            min_gain_pct = df['GAIN %'].min()
            max_gain_pct = df['GAIN %'].max()
            
            color_scale_config = {}
            
            if min_gain_pct >= 0:
                color_scale_config['color_continuous_scale'] = ['#FFC300', '#10b981']
                color_scale_config['range_color'] = [min_gain_pct, max_gain_pct]
            elif max_gain_pct <= 0:
                color_scale_config['color_continuous_scale'] = ['#f87171', '#ef4444']
                color_scale_config['range_color'] = [min_gain_pct, max_gain_pct]
            else:
                color_scale_config['color_continuous_scale'] = ['#ef4444', '#FFC300', '#10b981']
                color_scale_config['color_continuous_midpoint'] = 0
            
            fig_treemap = px.treemap(
                df,
                path=['SYMBOL'],
                values='CURR. VALUE',
                color='GAIN %',
                **color_scale_config 
            )
            fig_treemap.update_layout(
                margin=dict(t=0, l=0, r=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#EAEAEA'
            )
            st.plotly_chart(fig_treemap, width='stretch')

        with tab2:
            # Portfolio Holdings Table
            st.markdown("""
                <div class='section'>
                    <div class='section-header'>
                        <h3 class='section-title'>Portfolio Holdings</h3>
                        <p class='section-subtitle'>Detailed view of all investments (Current Price is near real-time)</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            display_df = df[['ASSET NAME', 'SYMBOL', 'QUANTITY', 'AVERAGE PRICE', 'INVESTED', 
                             'CURRENT PRICE', 'CURR. VALUE', 'GAIN', 'GAIN %', 'WT']].copy()
            
            # Add rank column
            display_df['RANK'] = display_df['CURR. VALUE'].rank(ascending=False).astype(int)
            display_df = display_df.sort_values('RANK')
            
            # Format columns
            display_df['AVERAGE PRICE'] = display_df['AVERAGE PRICE'].apply(format_currency)
            display_df['INVESTED'] = display_df['INVESTED'].apply(format_currency)
            display_df['CURRENT PRICE'] = display_df['CURRENT PRICE'].apply(format_currency)
            
            def format_gain(x):
                color = 'var(--success-green)' if x >= 0 else 'var(--danger-red)'
                return f"<span style='color: {color}'>{format_currency(x)}</span>"
            
            def format_gain_pct(x):
                color = 'var(--success-green)' if x >= 0 else 'var(--danger-red)'
                return f"<span style='color: {color}'>{x:.2f}%</span>"

            display_df['CURR. VALUE'] = display_df['CURR. VALUE'].apply(format_currency)
            display_df['GAIN'] = display_df['GAIN'].apply(format_gain)
            display_df['GAIN %'] = display_df['GAIN %'].apply(format_gain_pct)
            display_df['WT'] = display_df['WT'].apply(lambda x: f"{x:.2f}%")
            
            display_cols = ['RANK', 'ASSET NAME', 'SYMBOL', 'QUANTITY', 'AVERAGE PRICE', 'CURRENT PRICE', 
                           'INVESTED', 'CURR. VALUE', 'GAIN', 'GAIN %', 'WT']
            display_df = display_df[display_cols]
            
            st.markdown(f"""
                <div class='table-container'>
                    <table class='table'>
                        {display_df.to_html(escape=False, index=False, classes='table')}
                    </table>
                </div>
            """, unsafe_allow_html=True)
            
            # Export button
            excel_data = to_excel(df)
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.download_button(
                "Export Raw Portfolio Data (Excel)",
                excel_data,
                file_name=f"Swing_portfolio_details_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheet.sheet"
            )
        
        with tab3:
            # Holdings Analytics Tab - Institutional Grade
            st.markdown("""
                <div class='section'>
                    <div class='section-header'>
                        <h3 class='section-title'>Holdings Analytics</h3>
                        <p class='section-subtitle'>Institutional-grade concentration, diversification & risk decomposition</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Calculate advanced metrics
            n_holdings = len(df)
            weights = df['WT'].values / 100  # Convert to decimal
            returns = df['GAIN %'].values / 100
            
            # Concentration metrics
            hhi = (df['WT'] ** 2).sum()
            effective_n = 10000 / hhi if hhi > 0 else n_holdings
            gini = 0
            if n_holdings > 1:
                sorted_weights = np.sort(weights)
                cum_weights = np.cumsum(sorted_weights)
                gini = 1 - 2 * np.sum(cum_weights) / (n_holdings * cum_weights[-1]) if cum_weights[-1] > 0 else 0
            
            # Diversification ratio (simplified)
            avg_weight = weights.mean()
            weight_std = weights.std()
            div_ratio = 1 / (hhi / 10000) if hhi > 0 else n_holdings
            
            # Row 1: Concentration Metrics
            st.markdown("#### Concentration Metrics")
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            
            with c1:
                st.markdown(f"""
                    <div class='metric-card primary'>
                        <h4>Holdings</h4>
                        <h2>{n_holdings}</h2>
                        <div class='sub-metric'>Unique positions</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with c2:
                top5 = metrics['Top 5 Concentration']
                cls = 'warning' if top5 > 60 else 'success'
                st.markdown(f"""
                    <div class='metric-card {cls}'>
                        <h4>Top 5</h4>
                        <h2>{top5:.1f}%</h2>
                        <div class='sub-metric'>Concentration</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with c3:
                top10 = df['WT'].nlargest(10).sum()
                cls = 'warning' if top10 > 80 else 'success'
                st.markdown(f"""
                    <div class='metric-card {cls}'>
                        <h4>Top 10</h4>
                        <h2>{top10:.1f}%</h2>
                        <div class='sub-metric'>Concentration</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with c4:
                st.markdown(f"""
                    <div class='metric-card info'>
                        <h4>Effective N</h4>
                        <h2>{effective_n:.1f}</h2>
                        <div class='sub-metric'>1/HHI equivalent</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with c5:
                cls = 'warning' if hhi > 1500 else 'success'
                st.markdown(f"""
                    <div class='metric-card {cls}'>
                        <h4>HHI</h4>
                        <h2>{hhi:.0f}</h2>
                        <div class='sub-metric'><1500 = diverse</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with c6:
                st.markdown(f"""
                    <div class='metric-card neutral'>
                        <h4>Gini Coeff</h4>
                        <h2>{gini:.2f}</h2>
                        <div class='sub-metric'>0=equal, 1=conc</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Row 2: Performance Distribution
            st.markdown("#### Performance Distribution")
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            
            profitable = (df['GAIN %'] > 0).sum()
            losing = (df['GAIN %'] < 0).sum()
            breakeven = n_holdings - profitable - losing
            win_rate = profitable / n_holdings * 100 if n_holdings > 0 else 0
            
            with c1:
                st.markdown(f"""
                    <div class='metric-card success'>
                        <h4>Winners</h4>
                        <h2>{profitable}</h2>
                        <div class='sub-metric'>Profitable</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with c2:
                st.markdown(f"""
                    <div class='metric-card danger'>
                        <h4>Losers</h4>
                        <h2>{losing}</h2>
                        <div class='sub-metric'>Underwater</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with c3:
                cls = 'success' if win_rate > 60 else 'warning' if win_rate > 40 else 'danger'
                st.markdown(f"""
                    <div class='metric-card {cls}'>
                        <h4>Win Rate</h4>
                        <h2>{win_rate:.0f}%</h2>
                        <div class='sub-metric'>Batting avg</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with c4:
                avg_gain = df['GAIN %'].mean()
                cls = 'success' if avg_gain > 0 else 'danger'
                st.markdown(f"""
                    <div class='metric-card {cls}'>
                        <h4>Avg Return</h4>
                        <h2>{avg_gain:+.1f}%</h2>
                        <div class='sub-metric'>Mean gain</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with c5:
                median_gain = df['GAIN %'].median()
                cls = 'success' if median_gain > 0 else 'danger'
                st.markdown(f"""
                    <div class='metric-card {cls}'>
                        <h4>Median Return</h4>
                        <h2>{median_gain:+.1f}%</h2>
                        <div class='sub-metric'>50th percentile</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with c6:
                gain_std = df['GAIN %'].std()
                st.markdown(f"""
                    <div class='metric-card warning'>
                        <h4>Return Dispersion</h4>
                        <h2>{gain_std:.1f}%</h2>
                        <div class='sub-metric'>Std deviation</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            
            # Charts Row
            col_pie, col_lorenz = st.columns(2)
            
            with col_pie:
                st.markdown("#### Weight Distribution")
                
                # Treemap for weight distribution
                fig_tree = px.treemap(
                    df,
                    path=['SYMBOL'],
                    values='WT',
                    color='GAIN %',
                    color_continuous_scale=['#ef4444', '#FFC300', '#10b981'],
                    color_continuous_midpoint=0
                )
                fig_tree.update_layout(
                    margin=dict(t=10, l=10, r=10, b=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#EAEAEA',
                    height=320
                )
                fig_tree.update_coloraxes(showscale=False)
                st.plotly_chart(fig_tree, use_container_width=True)
            
            with col_lorenz:
                st.markdown("#### Concentration Curve")
                
                # Lorenz curve
                sorted_weights = np.sort(df['WT'].values)[::-1]
                cum_weights = np.cumsum(sorted_weights)
                n = len(sorted_weights)
                
                fig_lorenz = go.Figure()
                
                # Perfect equality line
                fig_lorenz.add_trace(go.Scatter(
                    x=list(range(n + 1)),
                    y=[0] + list(np.linspace(0, 100, n)),
                    mode='lines',
                    name='Equal Weight',
                    line=dict(color='#888888', dash='dash', width=1)
                ))
                
                # Actual concentration curve
                fig_lorenz.add_trace(go.Scatter(
                    x=list(range(n + 1)),
                    y=[0] + list(cum_weights),
                    mode='lines+markers',
                    name='Portfolio',
                    line=dict(color='#FFC300', width=2),
                    marker=dict(size=4),
                    fill='tonexty',
                    fillcolor='rgba(255, 195, 0, 0.15)'
                ))
                
                # Key thresholds
                fig_lorenz.add_hline(y=50, line_dash="dot", line_color="#10b981", 
                                    annotation_text="50%", annotation_position="right")
                fig_lorenz.add_hline(y=80, line_dash="dot", line_color="#06b6d4",
                                    annotation_text="80%", annotation_position="right")
                
                fig_lorenz.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#EAEAEA"),
                    margin=dict(l=10, r=10, t=10, b=10),
                    xaxis=dict(title='# Holdings (ranked)', gridcolor='rgba(255,255,255,0.05)'),
                    yaxis=dict(title='Cumulative Weight (%)', gridcolor='rgba(255,255,255,0.05)', range=[0, 105]),
                    height=320,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig_lorenz, use_container_width=True)
            
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            
            # Risk Contribution Table
            st.markdown("#### Risk & Return Contribution")
            
            # Calculate contribution metrics
            contrib_df = df[['SYMBOL', 'ASSET NAME', 'WT', 'GAIN %', 'WEIGHTED RETURN %']].copy()
            contrib_df['Weight'] = contrib_df['WT'].apply(lambda x: f"{x:.2f}%")
            contrib_df['Return'] = contrib_df['GAIN %'].apply(lambda x: f"{x:+.2f}%")
            contrib_df['Contribution'] = contrib_df['WEIGHTED RETURN %'].apply(lambda x: f"{x:+.3f}%")
            
            # Risk contribution (simplified - weight^2 as proxy)
            contrib_df['Risk Weight'] = (contrib_df['WT'] ** 2) / hhi * 100
            contrib_df['Risk Contrib'] = contrib_df['Risk Weight'].apply(lambda x: f"{x:.1f}%")
            
            # Sort by contribution
            contrib_df = contrib_df.sort_values('WEIGHTED RETURN %', ascending=False)
            
            # Create horizontal bar chart
            fig_contrib = make_subplots(rows=1, cols=2, shared_yaxes=True,
                                       subplot_titles=('Return Contribution', 'Risk Contribution'),
                                       horizontal_spacing=0.02)
            
            colors_ret = ['#10b981' if x >= 0 else '#ef4444' for x in contrib_df['WEIGHTED RETURN %']]
            
            fig_contrib.add_trace(go.Bar(
                y=contrib_df['SYMBOL'],
                x=contrib_df['WEIGHTED RETURN %'],
                orientation='h',
                marker_color=colors_ret,
                text=[f"{x:.2f}%" for x in contrib_df['WEIGHTED RETURN %']],
                textposition='outside',
                textfont=dict(size=9),
                showlegend=False
            ), row=1, col=1)
            
            fig_contrib.add_trace(go.Bar(
                y=contrib_df['SYMBOL'],
                x=contrib_df['Risk Weight'],
                orientation='h',
                marker_color='#FFC300',
                text=[f"{x:.1f}%" for x in contrib_df['Risk Weight']],
                textposition='outside',
                textfont=dict(size=9),
                showlegend=False
            ), row=1, col=2)
            
            fig_contrib.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#EAEAEA", size=10),
                margin=dict(l=10, r=60, t=40, b=10),
                height=max(350, n_holdings * 22 + 60),
                showlegend=False
            )
            
            fig_contrib.update_xaxes(gridcolor='rgba(255,255,255,0.05)')
            fig_contrib.update_yaxes(gridcolor='rgba(255,255,255,0.05)')
            
            st.plotly_chart(fig_contrib, use_container_width=True)
            
            # Summary Statistics in expander
            with st.expander("📊 Detailed Statistics", expanded=False):
                col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                
                with col_s1:
                    st.markdown("**Weight Stats**")
                    st.markdown(f"""
                    - Mean: **{df['WT'].mean():.2f}%**
                    - Median: **{df['WT'].median():.2f}%**
                    - Std: **{df['WT'].std():.2f}%**
                    - Max: **{df['WT'].max():.2f}%**
                    - Min: **{df['WT'].min():.2f}%**
                    """)
                
                with col_s2:
                    st.markdown("**Return Stats**")
                    st.markdown(f"""
                    - Mean: **{df['GAIN %'].mean():.2f}%**
                    - Median: **{df['GAIN %'].median():.2f}%**
                    - Std: **{df['GAIN %'].std():.2f}%**
                    - Max: **{df['GAIN %'].max():.2f}%**
                    - Min: **{df['GAIN %'].min():.2f}%**
                    """)
                
                with col_s3:
                    st.markdown("**Concentration**")
                    st.markdown(f"""
                    - Top 1: **{df['WT'].max():.1f}%**
                    - Top 3: **{df['WT'].nlargest(3).sum():.1f}%**
                    - Top 5: **{df['WT'].nlargest(5).sum():.1f}%**
                    - Top 10: **{df['WT'].nlargest(10).sum():.1f}%**
                    - Bottom 50%: **{df['WT'].nsmallest(n_holdings//2).sum():.1f}%**
                    """)
                
                with col_s4:
                    st.markdown("**Diversification**")
                    st.markdown(f"""
                    - HHI: **{hhi:.0f}**
                    - Effective N: **{effective_n:.1f}**
                    - Gini: **{gini:.3f}**
                    - Div Ratio: **{div_ratio:.2f}**
                    - Entropy: **{-np.sum(weights * np.log(weights + 1e-10)):.2f}**
                    """)
    
    # =========================================================================
    # ANALYSIS MODE
    # =========================================================================
    if view_mode == "📉 Analysis Mode":
        render_analysis_mode(df, metrics)
    
    # =========================================================================
    # FOOTER
    # =========================================================================
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    current_time_ist = ist_now.strftime("%Y-%m-%d %H:%M:%S IST")
    st.caption(f"© 2026 {PRODUCT_NAME} | {COMPANY} | {VERSION} | {current_time_ist}")


# =========================================================================
# ANALYSIS MODE - INSTITUTIONAL GRADE ANALYTICS
# =========================================================================

BENCHMARKS = {
    'NIFTY 50': '^NSEI',
    'NIFTY 500': '^CRSLDX'
}

TIMEFRAMES = {
    '1W': 7,
    '1M': 30,
    '3M': 90,
    '6M': 180,
    'YTD': None,  # Special handling
    '1Y': 365,
    '2Y': 730,
    '5Y': 1825,
    'MAX': 3650
}

@st.cache_data(ttl=300)
def fetch_analysis_data(symbols, days_back):
    """Fetch historical data for portfolio and benchmarks."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    tickers = [f"{s}.NS" for s in symbols]
    benchmark_tickers = list(BENCHMARKS.values())
    all_tickers = tickers + benchmark_tickers
    
    try:
        data = yf.download(
            tickers=all_tickers,
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d'),
            interval='1d',
            progress=False,
            threads=True
        )
        
        if data.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        close = data['Close']
        
        # Handle single ticker case
        if len(all_tickers) == 1:
            close = close.to_frame()
            close.columns = all_tickers
        
        # Split portfolio and benchmark
        portfolio_cols = [f"{s}.NS" for s in symbols]
        benchmark_cols = benchmark_tickers
        
        portfolio_df = close[[c for c in portfolio_cols if c in close.columns]].copy()
        portfolio_df.columns = [c.replace('.NS', '') for c in portfolio_df.columns]
        
        benchmark_df = close[[c for c in benchmark_cols if c in close.columns]].copy()
        rename_map = {v: k for k, v in BENCHMARKS.items()}
        benchmark_df.columns = [rename_map.get(c, c) for c in benchmark_df.columns]
        
        return portfolio_df, benchmark_df
        
    except Exception as e:
        return pd.DataFrame(), pd.DataFrame()


def compute_metrics(returns, benchmark_returns=None, rf_rate=0.065):
    """Compute institutional-grade performance metrics."""
    m = {}
    
    if returns.empty or len(returns) < 2:
        return m
    
    # Period metrics
    total_ret = (1 + returns).prod() - 1
    n_days = len(returns)
    ann_factor = 252 / n_days
    
    m['total_return'] = total_ret * 100
    m['cagr'] = ((1 + total_ret) ** ann_factor - 1) * 100
    
    # Volatility
    daily_vol = returns.std()
    m['volatility'] = daily_vol * np.sqrt(252) * 100
    m['daily_vol'] = daily_vol * 100
    
    # Drawdown
    cum = (1 + returns).cumprod()
    peak = cum.expanding().max()
    dd = (cum - peak) / peak
    m['max_drawdown'] = dd.min() * 100
    m['drawdown_series'] = dd * 100
    
    # Risk-adjusted ratios
    rf_daily = rf_rate / 252
    excess = returns - rf_daily
    
    m['sharpe'] = (excess.mean() / daily_vol * np.sqrt(252)) if daily_vol > 0 else 0
    
    downside = returns[returns < 0]
    downside_vol = downside.std() if len(downside) > 0 else daily_vol
    m['sortino'] = (excess.mean() / downside_vol * np.sqrt(252)) if downside_vol > 0 else 0
    
    m['calmar'] = m['cagr'] / abs(m['max_drawdown']) if m['max_drawdown'] != 0 else 0
    
    # VaR and CVaR
    m['var_95'] = np.percentile(returns, 5) * 100
    m['var_99'] = np.percentile(returns, 1) * 100
    var_threshold = np.percentile(returns, 5)
    tail = returns[returns <= var_threshold]
    m['cvar_95'] = tail.mean() * 100 if len(tail) > 0 else m['var_95']
    
    # Win rate
    m['win_rate'] = (returns > 0).mean() * 100
    m['win_days'] = (returns > 0).sum()
    m['lose_days'] = (returns < 0).sum()
    
    # Best/Worst
    m['best_day'] = returns.max() * 100
    m['worst_day'] = returns.min() * 100
    
    # Skew and Kurtosis
    m['skewness'] = returns.skew()
    m['kurtosis'] = returns.kurtosis()
    
    # Profit Factor
    gains = returns[returns > 0].sum()
    losses = abs(returns[returns < 0].sum())
    m['profit_factor'] = gains / losses if losses > 0 else float('inf')
    
    # Benchmark-relative metrics
    if benchmark_returns is not None and len(benchmark_returns) > 10:
        aligned = pd.concat([returns, benchmark_returns], axis=1).dropna()
        if len(aligned) > 10:
            p_ret = aligned.iloc[:, 0]
            b_ret = aligned.iloc[:, 1]
            
            # Beta
            cov = np.cov(p_ret, b_ret)[0, 1]
            var_b = b_ret.var()
            m['beta'] = cov / var_b if var_b > 0 else 1
            
            # Alpha (annualized)
            b_total = (1 + b_ret).prod() - 1
            b_cagr = ((1 + b_total) ** ann_factor - 1)
            p_cagr = m['cagr'] / 100
            m['alpha'] = (p_cagr - (rf_rate + m['beta'] * (b_cagr - rf_rate))) * 100
            
            # Correlation and R-squared
            m['correlation'] = p_ret.corr(b_ret)
            m['r_squared'] = m['correlation'] ** 2
            
            # Tracking Error
            tracking = (p_ret - b_ret).std() * np.sqrt(252)
            m['tracking_error'] = tracking * 100
            
            # Information Ratio
            excess_ret = p_cagr - b_cagr
            m['info_ratio'] = excess_ret / tracking if tracking > 0 else 0
            
            # Treynor Ratio
            m['treynor'] = (p_cagr - rf_rate) / m['beta'] if m['beta'] != 0 else 0
            
            # Up/Down Capture
            up_mask = b_ret > 0
            down_mask = b_ret < 0
            
            if up_mask.sum() > 0:
                up_p = (1 + p_ret[up_mask]).prod()
                up_b = (1 + b_ret[up_mask]).prod()
                m['up_capture'] = (up_p / up_b) * 100 if up_b > 0 else 100
            else:
                m['up_capture'] = 100
                
            if down_mask.sum() > 0:
                down_p = (1 + p_ret[down_mask]).prod()
                down_b = (1 + b_ret[down_mask]).prod()
                m['down_capture'] = (down_p / down_b) * 100 if down_b > 0 else 100
            else:
                m['down_capture'] = 100
            
            m['benchmark_return'] = b_total * 100
    
    return m


def render_analysis_mode(df, metrics):
    """Render Bloomberg Terminal style analytics."""
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # =========================================================================
    # HEADER & TIMEFRAME SELECTOR
    # =========================================================================
    
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
            <div>
                <h2 style="margin: 0; color: #FFC300;">Portfolio Analytics Terminal</h2>
                <p style="margin: 0; color: #888888; font-size: 0.9rem;">Institutional-Grade Performance Analysis</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'tf_selected' not in st.session_state:
        st.session_state.tf_selected = '1Y'
    
    # Timeframe buttons row
    tf_cols = st.columns(len(TIMEFRAMES))
    for i, tf in enumerate(TIMEFRAMES.keys()):
        with tf_cols[i]:
            btn_type = "primary" if st.session_state.tf_selected == tf else "secondary"
            if st.button(tf, key=f"tf_{tf}", use_container_width=True, type=btn_type):
                st.session_state.tf_selected = tf
                st.rerun()
    
    # Calculate days for selected timeframe
    selected_tf = st.session_state.tf_selected
    if selected_tf == 'YTD':
        today = datetime.now()
        days_back = (today - datetime(today.year, 1, 1)).days + 1
    else:
        days_back = TIMEFRAMES[selected_tf]
    
    # Benchmark selector
    col_bench, col_spacer = st.columns([1, 4])
    with col_bench:
        benchmark_choice = st.selectbox(
            "Benchmark",
            options=['NIFTY 50', 'NIFTY 500', 'Both'],
            index=0,
            label_visibility="collapsed"
        )
    
    # =========================================================================
    # FETCH DATA
    # =========================================================================
    
    symbols = df['SYMBOL'].tolist()
    quantities = df.set_index('SYMBOL')['QUANTITY'].to_dict()
    
    with st.spinner(f"Loading {selected_tf} data..."):
        portfolio_prices, benchmark_prices = fetch_analysis_data(symbols, days_back)
    
    if portfolio_prices.empty:
        st.error("Unable to fetch historical data. Please try again.")
        return
    
    # Build portfolio value series
    port_value = pd.DataFrame(index=portfolio_prices.index)
    for sym in portfolio_prices.columns:
        if sym in quantities:
            port_value[sym] = portfolio_prices[sym] * quantities[sym]
    port_value['Portfolio'] = port_value.sum(axis=1)
    port_value = port_value['Portfolio'].dropna()
    
    # Calculate returns
    port_returns = port_value.pct_change().dropna()
    
    # Get benchmark returns
    bench_returns = None
    if not benchmark_prices.empty:
        if benchmark_choice == 'Both':
            bench_col = 'NIFTY 50'  # Use NIFTY 50 for metrics
        else:
            bench_col = benchmark_choice
        if bench_col in benchmark_prices.columns:
            bench_returns = benchmark_prices[bench_col].pct_change().dropna()
    
    # Compute metrics
    m = compute_metrics(port_returns, bench_returns)
    
    # =========================================================================
    # MAIN COMPARISON CHART
    # =========================================================================
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Normalize to 100
    port_norm = (port_value / port_value.iloc[0]) * 100
    
    fig = go.Figure()
    
    # Portfolio trace
    port_ret_display = m.get('total_return', 0)
    fig.add_trace(go.Scatter(
        x=port_norm.index,
        y=port_norm.values,
        mode='lines',
        name=f'Portfolio ({port_ret_display:+.2f}%)',
        line=dict(color='#FFC300', width=2.5),
        hovertemplate='%{x|%b %d, %Y}<br>Portfolio: %{y:.2f}<extra></extra>'
    ))
    
    # Benchmark traces
    if not benchmark_prices.empty:
        colors = {'NIFTY 50': '#06b6d4', 'NIFTY 500': '#8b5cf6'}
        benchmarks_to_show = ['NIFTY 50', 'NIFTY 500'] if benchmark_choice == 'Both' else [benchmark_choice]
        
        for bench_name in benchmarks_to_show:
            if bench_name in benchmark_prices.columns:
                bench_series = benchmark_prices[bench_name].dropna()
                if len(bench_series) > 0:
                    bench_norm = (bench_series / bench_series.iloc[0]) * 100
                    bench_ret = ((bench_series.iloc[-1] / bench_series.iloc[0]) - 1) * 100
                    fig.add_trace(go.Scatter(
                        x=bench_norm.index,
                        y=bench_norm.values,
                        mode='lines',
                        name=f'{bench_name} ({bench_ret:+.2f}%)',
                        line=dict(color=colors.get(bench_name, '#888888'), width=2, dash='dot'),
                        hovertemplate=f'%{{x|%b %d, %Y}}<br>{bench_name}: %{{y:.2f}}<extra></extra>'
                    ))
    
    # Layout
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#EAEAEA", size=12),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=True,
            showspikes=True,
            spikecolor='#FFC300',
            spikethickness=1,
            spikedash='dot'
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=True,
            title='',
            side='right',
            showspikes=True,
            spikecolor='#FFC300',
            spikethickness=1,
            spikedash='dot'
        ),
        height=420,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(0,0,0,0)',
            font=dict(size=11)
        ),
        hovermode='x unified'
    )
    
    # Add range selector and crosshair
    fig.update_xaxes(
        rangeslider=dict(visible=False),
        rangeselector=dict(visible=False)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d']
    })
    
    # =========================================================================
    # PERFORMANCE SUMMARY - ROW 1 (Returns & Risk-Adjusted)
    # =========================================================================
    
    st.markdown("#### Returns & Risk-Adjusted Performance")
    
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    
    with c1:
        val = m.get('total_return', 0)
        cls = 'success' if val >= 0 else 'danger'
        st.markdown(f"""
            <div class='metric-card {cls}'>
                <h4>Period Return</h4>
                <h2>{val:+.2f}%</h2>
                <div class='sub-metric'>CAGR: {m.get('cagr', 0):+.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c2:
        alpha = m.get('alpha', 0)
        cls = 'success' if alpha > 0 else 'danger' if alpha < 0 else 'neutral'
        st.markdown(f"""
            <div class='metric-card {cls}'>
                <h4>Alpha</h4>
                <h2>{alpha:+.2f}%</h2>
                <div class='sub-metric'>Excess return</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c3:
        sharpe = m.get('sharpe', 0)
        cls = 'success' if sharpe > 1 else 'warning' if sharpe > 0.5 else 'danger'
        st.markdown(f"""
            <div class='metric-card {cls}'>
                <h4>Sharpe</h4>
                <h2>{sharpe:.2f}</h2>
                <div class='sub-metric'>Rf = 6.5%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c4:
        sortino = m.get('sortino', 0)
        cls = 'success' if sortino > 1.5 else 'warning' if sortino > 0.5 else 'danger'
        st.markdown(f"""
            <div class='metric-card {cls}'>
                <h4>Sortino</h4>
                <h2>{sortino:.2f}</h2>
                <div class='sub-metric'>Downside risk</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c5:
        calmar = m.get('calmar', 0)
        cls = 'success' if calmar > 1 else 'warning' if calmar > 0.5 else 'danger'
        st.markdown(f"""
            <div class='metric-card {cls}'>
                <h4>Calmar</h4>
                <h2>{calmar:.2f}</h2>
                <div class='sub-metric'>Return/MaxDD</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c6:
        ir = m.get('info_ratio', 0)
        cls = 'success' if ir > 0.5 else 'warning' if ir > 0 else 'danger'
        st.markdown(f"""
            <div class='metric-card {cls}'>
                <h4>Info Ratio</h4>
                <h2>{ir:.2f}</h2>
                <div class='sub-metric'>Active return/TE</div>
            </div>
        """, unsafe_allow_html=True)
    
    # =========================================================================
    # ROW 2 - RISK METRICS
    # =========================================================================
    
    st.markdown("#### Risk Metrics")
    
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    
    with c1:
        vol = m.get('volatility', 0)
        st.markdown(f"""
            <div class='metric-card warning'>
                <h4>Volatility</h4>
                <h2>{vol:.1f}%</h2>
                <div class='sub-metric'>Annualized</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c2:
        mdd = m.get('max_drawdown', 0)
        cls = 'danger' if mdd < -20 else 'warning' if mdd < -10 else 'success'
        st.markdown(f"""
            <div class='metric-card {cls}'>
                <h4>Max Drawdown</h4>
                <h2>{mdd:.1f}%</h2>
                <div class='sub-metric'>Peak to trough</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c3:
        var95 = m.get('var_95', 0)
        st.markdown(f"""
            <div class='metric-card danger'>
                <h4>VaR (95%)</h4>
                <h2>{var95:.2f}%</h2>
                <div class='sub-metric'>Daily at risk</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c4:
        cvar = m.get('cvar_95', 0)
        st.markdown(f"""
            <div class='metric-card danger'>
                <h4>CVaR (95%)</h4>
                <h2>{cvar:.2f}%</h2>
                <div class='sub-metric'>Expected shortfall</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c5:
        beta = m.get('beta', 1)
        cls = 'warning' if beta > 1.2 else 'info' if beta < 0.8 else 'neutral'
        st.markdown(f"""
            <div class='metric-card {cls}'>
                <h4>Beta</h4>
                <h2>{beta:.2f}</h2>
                <div class='sub-metric'>Market sensitivity</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c6:
        te = m.get('tracking_error', 0)
        st.markdown(f"""
            <div class='metric-card info'>
                <h4>Tracking Error</h4>
                <h2>{te:.1f}%</h2>
                <div class='sub-metric'>vs Benchmark</div>
            </div>
        """, unsafe_allow_html=True)
    
    # =========================================================================
    # ROW 3 - BENCHMARK COMPARISON
    # =========================================================================
    
    st.markdown("#### Benchmark Comparison")
    
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    
    with c1:
        bench_ret = m.get('benchmark_return', 0)
        cls = 'success' if bench_ret >= 0 else 'danger'
        st.markdown(f"""
            <div class='metric-card {cls}'>
                <h4>Benchmark</h4>
                <h2>{bench_ret:+.1f}%</h2>
                <div class='sub-metric'>{benchmark_choice}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c2:
        excess = m.get('total_return', 0) - m.get('benchmark_return', 0)
        cls = 'success' if excess > 0 else 'danger'
        st.markdown(f"""
            <div class='metric-card {cls}'>
                <h4>Excess Return</h4>
                <h2>{excess:+.1f}%</h2>
                <div class='sub-metric'>vs Benchmark</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c3:
        up_cap = m.get('up_capture', 100)
        cls = 'success' if up_cap > 100 else 'warning'
        st.markdown(f"""
            <div class='metric-card {cls}'>
                <h4>Up Capture</h4>
                <h2>{up_cap:.0f}%</h2>
                <div class='sub-metric'>Bull market</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c4:
        down_cap = m.get('down_capture', 100)
        cls = 'success' if down_cap < 100 else 'warning'
        st.markdown(f"""
            <div class='metric-card {cls}'>
                <h4>Down Capture</h4>
                <h2>{down_cap:.0f}%</h2>
                <div class='sub-metric'>Bear market</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c5:
        r2 = m.get('r_squared', 0)
        st.markdown(f"""
            <div class='metric-card info'>
                <h4>R-Squared</h4>
                <h2>{r2:.2f}</h2>
                <div class='sub-metric'>Explained variance</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c6:
        corr = m.get('correlation', 0)
        st.markdown(f"""
            <div class='metric-card info'>
                <h4>Correlation</h4>
                <h2>{corr:.2f}</h2>
                <div class='sub-metric'>vs Benchmark</div>
            </div>
        """, unsafe_allow_html=True)
    
    # =========================================================================
    # DRAWDOWN & DISTRIBUTION CHARTS
    # =========================================================================
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col_dd, col_dist = st.columns(2)
    
    with col_dd:
        st.markdown("#### Drawdown Analysis")
        
        dd_series = m.get('drawdown_series', pd.Series())
        if len(dd_series) > 0:
            fig_dd = go.Figure()
            fig_dd.add_trace(go.Scatter(
                x=dd_series.index,
                y=dd_series.values,
                mode='lines',
                fill='tozeroy',
                line=dict(color='#ef4444', width=1),
                fillcolor='rgba(239, 68, 68, 0.3)',
                hovertemplate='%{x|%b %d, %Y}<br>Drawdown: %{y:.2f}%<extra></extra>'
            ))
            
            fig_dd.add_hline(
                y=m.get('max_drawdown', 0),
                line_dash="dash",
                line_color="#FFC300",
                annotation_text=f"Max: {m.get('max_drawdown', 0):.1f}%",
                annotation_position="right"
            )
            
            fig_dd.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#EAEAEA"),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title=''),
                height=280,
                showlegend=False
            )
            st.plotly_chart(fig_dd, use_container_width=True)
    
    with col_dist:
        st.markdown("#### Returns Distribution")
        
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=port_returns * 100,
            nbinsx=40,
            marker_color='#FFC300',
            opacity=0.75,
            hovertemplate='Return: %{x:.2f}%<br>Count: %{y}<extra></extra>'
        ))
        
        fig_hist.add_vline(x=0, line_dash="dash", line_color="#888888", line_width=1)
        fig_hist.add_vline(
            x=port_returns.mean() * 100,
            line_dash="dot",
            line_color="#10b981",
            annotation_text=f"μ: {port_returns.mean()*100:.2f}%",
            annotation_position="top"
        )
        fig_hist.add_vline(
            x=m.get('var_95', 0),
            line_dash="dash",
            line_color="#ef4444",
            annotation_text=f"VaR: {m.get('var_95', 0):.1f}%",
            annotation_position="bottom left"
        )
        
        fig_hist.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#EAEAEA"),
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title='Daily Return (%)', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='', gridcolor='rgba(255,255,255,0.05)'),
            height=280,
            showlegend=False
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # =========================================================================
    # ROLLING METRICS
    # =========================================================================
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### Rolling Analytics (63-day)")
    
    window = min(63, len(port_returns) - 1)
    
    if window > 20:
        col_rs, col_rb = st.columns(2)
        
        with col_rs:
            # Rolling Sharpe
            roll_mean = port_returns.rolling(window).mean()
            roll_std = port_returns.rolling(window).std()
            roll_sharpe = (roll_mean / roll_std) * np.sqrt(252)
            roll_sharpe = roll_sharpe.dropna()
            
            fig_rs = go.Figure()
            fig_rs.add_trace(go.Scatter(
                x=roll_sharpe.index,
                y=roll_sharpe.values,
                mode='lines',
                line=dict(color='#FFC300', width=1.5),
                hovertemplate='%{x|%b %d}<br>Sharpe: %{y:.2f}<extra></extra>'
            ))
            fig_rs.add_hline(y=1, line_dash="dash", line_color="#10b981", annotation_text="Target", annotation_position="right")
            fig_rs.add_hline(y=0, line_dash="dash", line_color="#888888")
            
            fig_rs.update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#EAEAEA"),
                margin=dict(l=10, r=10, t=30, b=10),
                title=dict(text="Rolling Sharpe Ratio", font=dict(size=13)),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                height=260,
                showlegend=False
            )
            st.plotly_chart(fig_rs, use_container_width=True)
        
        with col_rb:
            # Rolling Beta
            if bench_returns is not None and len(bench_returns) > window:
                aligned = pd.concat([port_returns, bench_returns], axis=1).dropna()
                aligned.columns = ['Port', 'Bench']
                
                roll_betas = []
                roll_dates = []
                
                for i in range(window, len(aligned)):
                    w = aligned.iloc[i-window:i]
                    cov = np.cov(w['Port'], w['Bench'])[0, 1]
                    var = w['Bench'].var()
                    roll_betas.append(cov / var if var > 0 else 1)
                    roll_dates.append(aligned.index[i])
                
                fig_rb = go.Figure()
                fig_rb.add_trace(go.Scatter(
                    x=roll_dates,
                    y=roll_betas,
                    mode='lines',
                    line=dict(color='#06b6d4', width=1.5),
                    hovertemplate='%{x|%b %d}<br>Beta: %{y:.2f}<extra></extra>'
                ))
                fig_rb.add_hline(y=1, line_dash="dash", line_color="#888888", annotation_text="Market", annotation_position="right")
                
                fig_rb.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#EAEAEA"),
                    margin=dict(l=10, r=10, t=30, b=10),
                    title=dict(text="Rolling Beta", font=dict(size=13)),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                    height=260,
                    showlegend=False
                )
                st.plotly_chart(fig_rb, use_container_width=True)
    
    # =========================================================================
    # MONTHLY RETURNS HEATMAP
    # =========================================================================
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### Monthly Returns Heatmap")
    
    monthly = port_value.resample('ME').last().pct_change().dropna() * 100
    
    if len(monthly) > 1:
        monthly_df = pd.DataFrame({
            'Year': monthly.index.year,
            'Month': monthly.index.month,
            'Return': monthly.values
        })
        
        pivot = monthly_df.pivot_table(values='Return', index='Year', columns='Month', aggfunc='first')
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        pivot.columns = [month_names[c-1] for c in pivot.columns]
        
        # Add YTD column
        yearly = port_value.resample('YE').last().pct_change().dropna() * 100
        yearly_dict = {idx.year: val for idx, val in yearly.items()}
        pivot['YTD'] = pivot.index.map(lambda y: yearly_dict.get(y, np.nan))
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale=[[0, '#ef4444'], [0.5, '#1A1A1A'], [1, '#10b981']],
            zmid=0,
            text=[[f"{v:.1f}%" if pd.notna(v) else "" for v in row] for row in pivot.values],
            texttemplate="%{text}",
            textfont=dict(size=10, color="#EAEAEA"),
            hovertemplate="Year: %{y}<br>%{x}: %{z:.2f}%<extra></extra>",
            showscale=False
        ))
        
        fig_heat.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#EAEAEA"),
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(side='top', tickangle=0),
            yaxis=dict(autorange='reversed'),
            height=max(150, len(pivot) * 35 + 50)
        )
        
        st.plotly_chart(fig_heat, use_container_width=True)
    
    # =========================================================================
    # HOLDING ATTRIBUTION
    # =========================================================================
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("#### Holding Attribution")
    
    attribution = []
    for sym in symbols:
        if sym in portfolio_prices.columns:
            prices = portfolio_prices[sym].dropna()
            if len(prices) > 1:
                ret = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
                wt = df[df['SYMBOL'] == sym]['WT'].values[0] if 'WT' in df.columns else 0
                contrib = ret * wt / 100
                attribution.append({
                    'Symbol': sym,
                    'Return': ret,
                    'Weight': wt,
                    'Contribution': contrib
                })
    
    if attribution:
        attr_df = pd.DataFrame(attribution).sort_values('Contribution', ascending=True)
        
        fig_attr = go.Figure()
        
        colors = ['#10b981' if x >= 0 else '#ef4444' for x in attr_df['Contribution']]
        
        fig_attr.add_trace(go.Bar(
            y=attr_df['Symbol'],
            x=attr_df['Contribution'],
            orientation='h',
            marker_color=colors,
            text=[f"{x:+.2f}%" for x in attr_df['Contribution']],
            textposition='outside',
            textfont=dict(size=10),
            hovertemplate="<b>%{y}</b><br>Return: %{customdata[0]:.1f}%<br>Weight: %{customdata[1]:.1f}%<br>Contribution: %{x:.2f}%<extra></extra>",
            customdata=attr_df[['Return', 'Weight']].values
        ))
        
        fig_attr.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#EAEAEA"),
            margin=dict(l=10, r=60, t=10, b=10),
            xaxis=dict(title='Contribution (%)', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='', gridcolor='rgba(255,255,255,0.05)'),
            height=max(300, len(attr_df) * 25 + 50),
            showlegend=False
        )
        
        st.plotly_chart(fig_attr, use_container_width=True)
    
    # =========================================================================
    # STATISTICS TABLE
    # =========================================================================
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    with st.expander("📋 Detailed Statistics", expanded=False):
        col_s1, col_s2, col_s3 = st.columns(3)
        
        with col_s1:
            st.markdown("**Performance**")
            st.markdown(f"""
            - Total Return: **{m.get('total_return', 0):+.2f}%**
            - CAGR: **{m.get('cagr', 0):+.2f}%**
            - Best Day: **{m.get('best_day', 0):+.2f}%**
            - Worst Day: **{m.get('worst_day', 0):.2f}%**
            - Win Rate: **{m.get('win_rate', 0):.1f}%** ({m.get('win_days', 0)}W / {m.get('lose_days', 0)}L)
            - Profit Factor: **{m.get('profit_factor', 0):.2f}**
            """)
        
        with col_s2:
            st.markdown("**Risk**")
            st.markdown(f"""
            - Volatility (Ann.): **{m.get('volatility', 0):.2f}%**
            - Daily Volatility: **{m.get('daily_vol', 0):.3f}%**
            - Max Drawdown: **{m.get('max_drawdown', 0):.2f}%**
            - VaR 95%: **{m.get('var_95', 0):.2f}%**
            - VaR 99%: **{m.get('var_99', 0):.2f}%**
            - CVaR 95%: **{m.get('cvar_95', 0):.2f}%**
            """)
        
        with col_s3:
            st.markdown("**Distribution**")
            st.markdown(f"""
            - Skewness: **{m.get('skewness', 0):.3f}**
            - Kurtosis: **{m.get('kurtosis', 0):.3f}**
            - Sharpe: **{m.get('sharpe', 0):.2f}**
            - Sortino: **{m.get('sortino', 0):.2f}**
            - Calmar: **{m.get('calmar', 0):.2f}**
            - Treynor: **{m.get('treynor', 0):.3f}**
            """)
    
    st.toast(f"Analytics loaded for {selected_tf}", icon="📊")


if __name__ == "__main__":
    import base64
    main()
