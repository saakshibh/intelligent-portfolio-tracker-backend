import yfinance as yf

def test_single_stock():
    print("--- DEBUG START ---")
    ticker_symbol = "TCS.NS"
    print(f"1. Attempting to fetch {ticker_symbol}...")

    try:
        ticker = yf.Ticker(ticker_symbol)
        # Fetching 5 days to ensure we get a valid row
        data = ticker.history(period="5d")

        if not data.empty:
            # Force all column names to lowercase to prevent KeyErrors
            data.columns = [c.lower() for c in data.columns]
            
            if 'close' in data.columns:
                price = data['close'].iloc[-1]
                print(f"2. Success! Current Price: {round(price, 2)} INR")
            else:
                print(f"2. ⚠️ Error: Columns found were {list(data.columns)}")
        else:
            print("2. ⚠️ Error: The data returned from Yahoo was empty.")
            
    except Exception as e:
        print(f"❌ A Python Error Occurred: {e}")

if __name__ == "__main__":
    test_single_stock()