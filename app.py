import streamlit as st
import yfinance as yf
import pandas as pd

# Set up Streamlit page
st.set_page_config(page_title="Valuation Dashboard", layout="centered")
st.title("📈 Valuation Multiples Dashboard")
st.write("Analyze a company's valuation using real-time financial data.")

# Input section
ticker = st.text_input("Enter a stock ticker (e.g. AAPL, MSFT, TSLA):", value="AAPL").upper()

def get_valuation_multiples(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    # Debug: Show raw data if needed
    # st.json(info)

    try:
        market_cap = info.get("marketCap", None)
        total_debt = info.get("totalDebt", 0)
        cash = info.get("totalCash", 0)
        ebitda = info.get("ebitda", None)
        revenue = info.get("totalRevenue", None)
        net_income = info.get("netIncome", None)
        price = info.get("currentPrice", None)

        # If essential data is missing, return None
        if market_cap is None or revenue is None or net_income is None or price is None:
            return None

        enterprise_value = market_cap + total_debt - cash if market_cap else None
        pe_ratio = market_cap / net_income if net_income else "N/A"
        ev_ebitda = enterprise_value / ebitda if ebitda and enterprise_value else "N/A"
        price_sales = market_cap / revenue if revenue else "N/A"

        data = {
            "Ticker": ticker,
            "Current Price ($)": price,
            "Market Cap ($B)": round(market_cap / 1e9, 2),
            "Enterprise Value ($B)": round(enterprise_value / 1e9, 2) if enterprise_value else "N/A",
            "P/E Ratio": round(pe_ratio, 2) if isinstance(pe_ratio, (int, float)) else "N/A",
            "EV/EBITDA": round(ev_ebitda, 2) if isinstance(ev_ebitda, (int, float)) else "N/A",
            "P/S Ratio": round(price_sales, 2) if isinstance(price_sales, (int, float)) else "N/A"
        }

        return pd.DataFrame([data])

    except Exception as e:
        st.error(f"Error retrieving data: {e}")
        return None

# Run on submit
if ticker:
    df = get_valuation_multiples(ticker)
    if df is not None:
        st.subheader("📊 Valuation Multiples")
        st.dataframe(df.style.format(precision=2))
    else:
        st.warning("⚠️ Not enough data available for this company. Try a major public company like AAPL or MSFT.")
