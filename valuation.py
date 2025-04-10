import yfinance as yf
import pandas as pd

def get_valuation_multiples(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    try:
        market_cap = info.get("marketCap")
        total_debt = info.get("totalDebt", 0)
        cash = info.get("totalCash", 0)
        ebitda = info.get("ebitda")
        revenue = info.get("totalRevenue")
        net_income = info.get("netIncome")
        shares_outstanding = info.get("sharesOutstanding")
        price = info.get("currentPrice")

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
        print(f"Error retrieving data: {e}")
        return None

# Example usage
ticker = input("Enter a stock ticker (e.g., AAPL, MSFT): ")
df = get_valuation_multiples(ticker.upper())
if df is not None:
    print(df.to_string(index=False))
