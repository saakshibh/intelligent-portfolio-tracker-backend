import numpy as np
import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def train_model(ticker_symbol):
    # 1. Download Historical Data with Multi-Level Fallback
    print(f"📥 Downloading history for {ticker_symbol}...")
    
    # Try 2 years first
    data = yf.download(ticker_symbol, period="2y", progress=False)
    
    # If 2y fails, try 1y, then 6mo
    if data.empty or len(data) < 60:
        print(f"⚠️ 2Y data unavailable for {ticker_symbol}, trying 1Y...")
        data = yf.download(ticker_symbol, period="1y", progress=False)
    
    if data.empty or len(data) < 60:
        print(f"⚠️ 1Y data unavailable, trying 6mo fallback...")
        data = yf.download(ticker_symbol, period="6mo", progress=False)

    if data.empty or len(data) < 60:
        print(f"❌ CRITICAL: Not enough data (need at least 60 days) for {ticker_symbol}")
        return None  # Return None so final_sync.py can handle the skip safely

    # FIX: Handle yfinance 0.2.x MultiIndex column structure
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    # Extract Close prices and reshape
    dataset = data['Close'].values.reshape(-1, 1)
    
    # 2. Scale the Data (0 to 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    # 3. Create Training Windows (60 days)
    x_train, y_train = [], []
    for i in range(60, len(scaled_data)):
        x_train.append(scaled_data[i-60:i, 0])
        y_train.append(scaled_data[i, 0])
    
    # Convert to numpy arrays
    x_train, y_train = np.array(x_train), np.array(y_train)
    
    # Safety Check: If window creation resulted in empty arrays
    if len(x_train) == 0:
        print(f"❌ Failed to create training windows for {ticker_symbol}")
        return None

    # Reshape for LSTM [samples, time steps, features]
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # 4. Build the LSTM Architecture
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
        Dropout(0.2), 
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        Dense(units=25),
        Dense(units=1) 
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # 5. Train the Model
    # Reduced epochs and batch size for faster laptop/hostel-wifi testing
    print("🧠 Training the 'Brain' (This involves heavy math)...")
    model.fit(x_train, y_train, batch_size=16, epochs=3, verbose=1) 
    
    print(f"✅ Model trained successfully for {ticker_symbol}!")
    return model, scaler

if __name__ == "__main__":
    # Test with a known ticker
    res = train_model("TCS.NS")
    if res:
        print("Test training complete.")