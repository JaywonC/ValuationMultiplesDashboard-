import streamlit as st
import yfinance as yf
import pandas as pd

# Set page config
st.set_page_config(page_title="Valuation Dashboard", layout="centered")

st.title("📈 Valuation Multiples Dashboard")
st.write("Analyze a company's valuation using real-time financial data.")

# Sidebar input
ticker = st.text_input("Enter a stock ticker (e.g. AAPL, MSFT, TSLA):", value="AAPL").upper()

def get_valuation_multiples(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    try:
        market_cap = info.get("marketCap", None)
        total_debt = info.get("totalDebt", 0)
        cash = info.get("totalCash", 0)
        ebitda = info.get("ebitda", None)
        revenue = info.get("totalRevenue", None)
        net_income = info.get("netIncome", None)
        shares_outstanding = info.get("sharesOutstanding", None)
        price = info.get("currentPrice", None)

        if not all([market_cap, ebitda, revenue, net_income]):
            return None

        enterprise_value = market_cap + total_debt - cash
        pe_ratio = market_cap / net_income if net_income else None
        ev_ebitda = enterprise_value / ebitda if ebitda else None
        price_sales = market_cap / revenue if revenue else None

        data = {
            "Ticker": ticker,
            "Price": price,
            "Market Cap ($B)": market_cap / 1e9,
            "Enterprise Value ($B)": enterprise_value / 1e9,
            "P/E Ratio": pe_ratio,
            "EV/EBITDA": ev_ebitda,
            "P/S Ratio": price_sales
        }

        return pd.DataFrame([data])

    except Exception as e:
        st.error(f"Error retrieving data: {e}")
        return None

# When user enters a ticker
if ticker:
    df = get_valuation_multiples(ticker)
    if df is not None:
        st.subheader("📊 Valuation Multiples")
        st.dataframe(df.style.format("{:.2f}"))
    else:
        st.warning("Not enough data available for this company.")
