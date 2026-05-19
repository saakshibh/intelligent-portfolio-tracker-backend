import pandas as pd
import numpy as np
import yfinance as yf
from database_manager import SupabaseManager
from sentiment_engine import get_sentiment
from lstm_model import train_model

def analyze_and_sync(tickers):
    db = SupabaseManager()
    
    if isinstance(tickers, str):
        tickers = [tickers]
    
    clean_watchlist = []
    for item in tickers:
        parts = str(item).split()
        ticker = parts[-1].strip().upper() 
        if ".NS" in ticker or "-USD" in ticker:
            clean_watchlist.append(ticker)

    for ticker in clean_watchlist:
        try:
            # 1. Get AI Sentiment AND News Snippets (Unpacking two values)
            print(f"🔍 Analyzing news & headlines for {ticker}...")
            sentiment_score, news_list = get_sentiment(ticker)
            
            # 2. Get AI Prediction
            print(f"🧠 Training/Loading LSTM for {ticker}...")
            training_result = train_model(ticker)
            
            if training_result is None: continue
                
            model, scaler = training_result
            data = yf.download(ticker, period="90d", progress=False)
            if data.empty: continue

            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
                
            recent_prices = data['Close'].values.reshape(-1, 1)
            current_price = float(recent_prices[-1][0])

            if len(recent_prices) < 60: continue

            # Run Prediction
            last_60_scaled = scaler.transform(recent_prices[-60:])
            X_test = np.reshape(np.array([last_60_scaled]), (1, 60, 1))
            pred_scaled = model.predict(X_test)
            final_pred = float(scaler.inverse_transform(pred_scaled)[0][0]) 
            
            # Smart Signal Logic
            price_change_pct = (final_pred - current_price) / current_price
            market_label = "Bullish" if price_change_pct > 0.02 else "Bearish" if price_change_pct < -0.02 else "Neutral"

            # 7-Day History
            recent_actuals = data['Close'].tail(7).values.flatten().tolist()
            history_data = []
            for i in range(len(recent_actuals)):
                history_data.append({
                    "day": f"D{i+1}",
                    "actual": round(float(recent_actuals[i]), 2),
                    "predicted": round(float(recent_actuals[i] * (1 + sentiment_score * 0.01)), 2)
                })

            # 3. Prepare Data (Adding news_snippets here)
            data_to_save = {
                "asset": ticker,
                "score": sentiment_score,
                "label": market_label, 
                "predicted_price": round(final_pred, 2),
                "history": history_data,
                "news_snippets": news_list # SAVES TO JSONB COLUMN
            }
            
            db.insert_data("market_sentiment", data_to_save) 
            print(f"🚀 SUCCESS: {ticker} (Deep Headlines + History) synced!")

        except Exception as e:
            print(f"❌ Error processing {ticker}: {str(e)}")

if __name__ == "__main__":
    watchlist = ["TCS.NS", "RELIANCE.NS", "WIPRO.NS"]
    analyze_and_sync(watchlist)