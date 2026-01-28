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
            # Holdings Analytics Tab
            st.markdown("""
                <div class='section'>
                    <div class='section-header'>
                        <h3 class='section-title'>Holdings Analytics</h3>
                        <p class='section-subtitle'>Advanced portfolio concentration and diversification metrics</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Key metrics cards
            col_h1, col_h2, col_h3, col_h4 = st.columns(4)
            
            with col_h1:
                st.markdown(f"""
                    <div class='metric-card primary'>
                        <h4>Total Holdings</h4>
                        <h2>{metrics['Number of Holdings']}</h2>
                        <div class='sub-metric'>Unique positions</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_h2:
                st.markdown(f"""
                    <div class='metric-card warning'>
                        <h4>Top 5 Concentration</h4>
                        <h2>{metrics['Top 5 Concentration']:.1f}%</h2>
                        <div class='sub-metric'>of portfolio value</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_h3:
                top_10_conc = df['WT'].nlargest(10).sum()
                st.markdown(f"""
                    <div class='metric-card info'>
                        <h4>Top 10 Concentration</h4>
                        <h2>{top_10_conc:.1f}%</h2>
                        <div class='sub-metric'>of portfolio value</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_h4:
                # Herfindahl-Hirschman Index (HHI) for concentration
                hhi = (df['WT'] ** 2).sum()
                effective_holdings = 10000 / hhi if hhi > 0 else 0
                st.markdown(f"""
                    <div class='metric-card neutral'>
                        <h4>Effective Holdings</h4>
                        <h2>{effective_holdings:.1f}</h2>
                        <div class='sub-metric'>HHI: {hhi:.0f}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            
            # Concentration breakdown
            col_conc1, col_conc2 = st.columns(2)
            
            with col_conc1:
                st.markdown("### Weight Distribution")
                
                # Create weight distribution chart
                sorted_by_weight = df.sort_values('WT', ascending=False)
                
                fig_weight = go.Figure()
                fig_weight.add_trace(go.Bar(
                    x=sorted_by_weight['SYMBOL'],
                    y=sorted_by_weight['WT'],
                    marker_color='#FFC300',
                    text=[f"{x:.1f}%" for x in sorted_by_weight['WT']],
                    textposition='outside',
                    textfont=dict(color='#EAEAEA', size=10)
                ))
                
                fig_weight.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#EAEAEA"),
                    margin=dict(l=0, r=0, t=30, b=0),
                    xaxis=dict(title='Symbol', tickangle=45, gridcolor='rgba(255,255,255,0.05)'),
                    yaxis=dict(title='Weight (%)', gridcolor='rgba(255,255,255,0.05)'),
                    height=350,
                    showlegend=False
                )
                st.plotly_chart(fig_weight, width='stretch')
            
            with col_conc2:
                st.markdown("### Cumulative Weight")
                
                # Cumulative weight chart
                sorted_by_weight['Cumulative WT'] = sorted_by_weight['WT'].cumsum()
                
                fig_cum = go.Figure()
                fig_cum.add_trace(go.Scatter(
                    x=list(range(1, len(sorted_by_weight) + 1)),
                    y=sorted_by_weight['Cumulative WT'],
                    mode='lines+markers',
                    line=dict(color='#FFC300', width=2),
                    marker=dict(size=6),
                    fill='tozeroy',
                    fillcolor='rgba(255, 195, 0, 0.1)'
                ))
                
                # Add reference lines
                fig_cum.add_hline(y=50, line_dash="dash", line_color="#888888", 
                                 annotation_text="50%", annotation_position="right")
                fig_cum.add_hline(y=80, line_dash="dash", line_color="#888888",
                                 annotation_text="80%", annotation_position="right")
                
                fig_cum.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#EAEAEA"),
                    margin=dict(l=0, r=0, t=30, b=0),
                    xaxis=dict(title='Number of Holdings', gridcolor='rgba(255,255,255,0.05)'),
                    yaxis=dict(title='Cumulative Weight (%)', gridcolor='rgba(255,255,255,0.05)', range=[0, 105]),
                    height=350,
                    showlegend=False
                )
                st.plotly_chart(fig_cum, width='stretch')
            
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            
            # Additional metrics table
            st.markdown("### Portfolio Statistics")
            
            # Calculate additional stats
            profitable_holdings = (df['GAIN %'] > 0).sum()
            losing_holdings = (df['GAIN %'] < 0).sum()
            avg_gain = df['GAIN %'].mean()
            median_gain = df['GAIN %'].median()
            avg_weight = df['WT'].mean()
            max_weight = df['WT'].max()
            min_weight = df['WT'].min()
            
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            
            with stats_col1:
                st.markdown(f"""
                    <div class='info-box'>
                        <h4>Performance Split</h4>
                        <p><span style='color: var(--success-green);'>Profitable: {profitable_holdings}</span> | 
                           <span style='color: var(--danger-red);'>Losing: {losing_holdings}</span></p>
                        <p>Win Rate: <strong>{profitable_holdings / len(df) * 100:.1f}%</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            
            with stats_col2:
                st.markdown(f"""
                    <div class='info-box'>
                        <h4>Return Statistics</h4>
                        <p>Average Gain: <strong>{avg_gain:.2f}%</strong></p>
                        <p>Median Gain: <strong>{median_gain:.2f}%</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            
            with stats_col3:
                st.markdown(f"""
                    <div class='info-box'>
                        <h4>Weight Statistics</h4>
                        <p>Average: <strong>{avg_weight:.2f}%</strong></p>
                        <p>Range: <strong>{min_weight:.2f}% - {max_weight:.2f}%</strong></p>
                    </div>
                """, unsafe_allow_html=True)
    
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
# ANALYSIS MODE FUNCTIONS
# =========================================================================

@st.cache_data(ttl=600)
def fetch_historical_prices(symbols, period='1y'):
    """Fetch historical prices for portfolio analysis."""
    if not symbols:
        return pd.DataFrame()
    
    tickers_with_suffix = [f"{s}.NS" for s in symbols]
    
    try:
        data = yf.download(
            tickers=tickers_with_suffix,
            period=period,
            interval='1d',
            progress=False,
            threads=True
        )
        
        if data.empty:
            return pd.DataFrame()
        
        close_prices = data['Close']
        
        # Rename columns to remove .NS suffix
        if len(tickers_with_suffix) == 1:
            close_prices = close_prices.to_frame()
            close_prices.columns = [symbols[0]]
        else:
            close_prices.columns = [col.replace('.NS', '') for col in close_prices.columns]
        
        return close_prices
        
    except Exception as e:
        st.error(f"Error fetching historical data: {e}")
        return pd.DataFrame()


def calculate_portfolio_time_series(df, historical_prices):
    """Calculate portfolio value over time."""
    if historical_prices.empty:
        return pd.DataFrame()
    
    # Get quantities for each symbol
    quantities = df.set_index('SYMBOL')['QUANTITY'].to_dict()
    
    # Calculate portfolio value for each date
    portfolio_values = pd.DataFrame(index=historical_prices.index)
    
    for symbol in historical_prices.columns:
        if symbol in quantities:
            portfolio_values[symbol] = historical_prices[symbol] * quantities[symbol]
    
    portfolio_values['Total Value'] = portfolio_values.sum(axis=1)
    portfolio_values['Daily Return %'] = portfolio_values['Total Value'].pct_change() * 100
    
    return portfolio_values


def render_analysis_mode(df, metrics):
    """Render the Analysis Mode dashboard."""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class='section'>
            <div class='section-header'>
                <h3 class='section-title'>📉 Portfolio Analysis Mode</h3>
                <p class='section-subtitle'>Historical performance tracking and time series analysis</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Time period selector
    col_period, col_custom = st.columns([1, 2])
    
    with col_period:
        period_options = {
            "1 Week": "5d",
            "1 Month": "1mo",
            "3 Months": "3mo",
            "6 Months": "6mo",
            "Year to Date": "ytd",
            "1 Year": "1y",
            "2 Years": "2y",
            "Max": "max"
        }
        selected_period = st.selectbox(
            "Select Time Period",
            options=list(period_options.keys()),
            index=5  # Default to 1 Year
        )
    
    # Fetch historical data
    symbols = df['SYMBOL'].tolist()
    
    with st.spinner("Fetching historical data..."):
        historical_prices = fetch_historical_prices(symbols, period_options[selected_period])
    
    if historical_prices.empty:
        st.warning("Could not fetch historical data. Please try again later.")
        return
    
    # Calculate portfolio time series
    portfolio_ts = calculate_portfolio_time_series(df, historical_prices)
    
    if portfolio_ts.empty:
        st.warning("Could not calculate portfolio time series.")
        return
    
    # =========================================================================
    # PERFORMANCE METRICS OVER PERIOD
    # =========================================================================
    
    start_value = portfolio_ts['Total Value'].iloc[0]
    end_value = portfolio_ts['Total Value'].iloc[-1]
    period_return = (end_value - start_value) / start_value * 100
    period_gain = end_value - start_value
    
    # Calculate additional metrics
    daily_returns = portfolio_ts['Daily Return %'].dropna()
    volatility = daily_returns.std() * np.sqrt(252)  # Annualized
    
    # Max Drawdown
    cumulative = (1 + daily_returns / 100).cumprod()
    peak = cumulative.expanding(min_periods=1).max()
    drawdown = (cumulative - peak) / peak * 100
    max_drawdown = drawdown.min()
    
    # Sharpe Ratio (assuming 6% risk-free rate for India)
    avg_daily_return = daily_returns.mean()
    risk_free_daily = 6 / 252
    sharpe = (avg_daily_return - risk_free_daily) / daily_returns.std() * np.sqrt(252) if daily_returns.std() > 0 else 0
    
    # Win Rate
    win_days = (daily_returns > 0).sum()
    total_days = len(daily_returns)
    win_rate = win_days / total_days * 100 if total_days > 0 else 0
    
    # Display period metrics
    st.markdown(f"### Performance Summary: {selected_period}")
    
    col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns(6)
    
    with col_m1:
        period_class = 'success' if period_return >= 0 else 'danger'
        st.markdown(f"""
            <div class='metric-card {period_class}'>
                <h4>Period Return</h4>
                <h2>{period_return:+.2f}%</h2>
                <div class='sub-metric'>{format_currency(period_gain)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_m2:
        st.markdown(f"""
            <div class='metric-card warning'>
                <h4>Volatility (Ann.)</h4>
                <h2>{volatility:.1f}%</h2>
                <div class='sub-metric'>Daily σ: {daily_returns.std():.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_m3:
        dd_class = 'danger' if max_drawdown < -10 else 'warning' if max_drawdown < -5 else 'success'
        st.markdown(f"""
            <div class='metric-card {dd_class}'>
                <h4>Max Drawdown</h4>
                <h2>{max_drawdown:.1f}%</h2>
                <div class='sub-metric'>Peak to trough</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_m4:
        sharpe_class = 'success' if sharpe > 1 else 'warning' if sharpe > 0 else 'danger'
        st.markdown(f"""
            <div class='metric-card {sharpe_class}'>
                <h4>Sharpe Ratio</h4>
                <h2>{sharpe:.2f}</h2>
                <div class='sub-metric'>Risk-adjusted return</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_m5:
        st.markdown(f"""
            <div class='metric-card info'>
                <h4>Win Rate</h4>
                <h2>{win_rate:.1f}%</h2>
                <div class='sub-metric'>{win_days}/{total_days} days</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_m6:
        best_day = daily_returns.max()
        worst_day = daily_returns.min()
        st.markdown(f"""
            <div class='metric-card neutral'>
                <h4>Best / Worst Day</h4>
                <h2 style='font-size: 1.25rem;'><span style='color: var(--success-green);'>+{best_day:.1f}%</span> / <span style='color: var(--danger-red);'>{worst_day:.1f}%</span></h2>
                <div class='sub-metric'>Single day extremes</div>
            </div>
        """, unsafe_allow_html=True)
    
    # =========================================================================
    # PORTFOLIO VALUE CHART
    # =========================================================================
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Portfolio Value Over Time")
    
    fig_value = go.Figure()
    
    fig_value.add_trace(go.Scatter(
        x=portfolio_ts.index,
        y=portfolio_ts['Total Value'],
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#FFC300', width=2),
        fill='tozeroy',
        fillcolor='rgba(255, 195, 0, 0.1)'
    ))
    
    fig_value.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#EAEAEA"),
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', showgrid=True),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', showgrid=True, title='Value (₹)'),
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_value, width='stretch')
    
    # =========================================================================
    # DAILY RETURNS DISTRIBUTION
    # =========================================================================
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### Daily Returns Distribution")
        
        fig_hist = go.Figure()
        
        # Color bars based on positive/negative
        colors = ['#10b981' if x >= 0 else '#ef4444' for x in daily_returns]
        
        fig_hist.add_trace(go.Histogram(
            x=daily_returns,
            nbinsx=50,
            marker_color='#FFC300',
            opacity=0.7
        ))
        
        # Add vertical line at 0
        fig_hist.add_vline(x=0, line_dash="dash", line_color="#888888", line_width=1)
        
        # Add mean line
        fig_hist.add_vline(x=daily_returns.mean(), line_dash="dot", line_color="#10b981", line_width=2,
                          annotation_text=f"Mean: {daily_returns.mean():.2f}%", annotation_position="top")
        
        fig_hist.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#EAEAEA"),
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(title='Daily Return (%)', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='Frequency', gridcolor='rgba(255,255,255,0.05)'),
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig_hist, width='stretch')
    
    with col_chart2:
        st.markdown("### Drawdown Over Time")
        
        fig_dd = go.Figure()
        
        fig_dd.add_trace(go.Scatter(
            x=drawdown.index,
            y=drawdown.values,
            mode='lines',
            name='Drawdown',
            line=dict(color='#ef4444', width=1.5),
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.2)'
        ))
        
        fig_dd.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#EAEAEA"),
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='Drawdown (%)', gridcolor='rgba(255,255,255,0.05)'),
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig_dd, width='stretch')
    
    # =========================================================================
    # INDIVIDUAL HOLDING PERFORMANCE
    # =========================================================================
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Individual Holding Performance")
    
    # Calculate period return for each holding
    holding_performance = []
    
    for symbol in df['SYMBOL'].tolist():
        if symbol in historical_prices.columns:
            start_price = historical_prices[symbol].iloc[0]
            end_price = historical_prices[symbol].iloc[-1]
            if pd.notna(start_price) and pd.notna(end_price) and start_price > 0:
                period_ret = (end_price - start_price) / start_price * 100
                holding_performance.append({
                    'Symbol': symbol,
                    'Start Price': start_price,
                    'End Price': end_price,
                    'Period Return %': period_ret
                })
    
    if holding_performance:
        perf_df = pd.DataFrame(holding_performance).sort_values('Period Return %', ascending=False)
        
        fig_holdings = go.Figure()
        
        colors = ['#10b981' if x >= 0 else '#ef4444' for x in perf_df['Period Return %']]
        
        fig_holdings.add_trace(go.Bar(
            x=perf_df['Symbol'],
            y=perf_df['Period Return %'],
            marker_color=colors,
            text=[f"{x:+.1f}%" for x in perf_df['Period Return %']],
            textposition='outside',
            textfont=dict(color='#EAEAEA', size=11)
        ))
        
        fig_holdings.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#EAEAEA"),
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(title='Symbol', gridcolor='rgba(255,255,255,0.05)', tickangle=45),
            yaxis=dict(title='Period Return (%)', gridcolor='rgba(255,255,255,0.05)'),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_holdings, width='stretch')
    
    st.toast(f"Analysis loaded for {selected_period}", icon="📊")


if __name__ == "__main__":
    import base64
    main()
