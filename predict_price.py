import numpy as np
import yfinance as yf
import pandas as pd
from lstm_model import train_model

def get_tomorrow_prediction(ticker_symbol):
    # 1. Train the model and get the scaler
    model, scaler = train_model(ticker_symbol)

    # 2. Fetch the most recent 60 days of data
    print(f"\n🔮 Fetching recent data for {ticker_symbol} prediction...")
    data = yf.download(ticker_symbol, period="90d")
    
    # Clean column names for yfinance consistency
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    recent_data = data['Close'].values.reshape(-1, 1)
    
    # 3. Prepare the input window (the last 60 days)
    last_60_days = recent_data[-60:]
    last_60_days_scaled = scaler.transform(last_60_days)
    
    X_test = []
    X_test.append(last_60_days_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # 4. Predict!
    pred_price_scaled = model.predict(X_test)
    pred_price = scaler.inverse_transform(pred_price_scaled)

    print(f"\n📈 PREDICTION RESULT for {ticker_symbol}:")
    print(f"The model predicts the next closing price will be: {round(float(pred_price[0][0]), 2)} INR")

if __name__ == "__main__":
    get_tomorrow_prediction("TCS.NS")