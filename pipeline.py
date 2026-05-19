import time
import yfinance as yf
from sentiment_engine import MarketSentiment
from database_manager import save_sentiment_to_cloud

def run_portfolio_update():
    # Watchlist containing both Indian Stocks and Global Crypto
    watchlist = ["TCS.NS", "RELIANCE.NS", "BTC-USD", "ETH-USD"]
    engine = MarketSentiment()
    
    print(f"🚀 Starting Automated Market Update...")
    
    for asset in watchlist:
        try:
            print(f"\nAnalyzing {asset}...")
            ticker = yf.Ticker(asset)
            news = ticker.news
            
            if not news:
                print(f"⚠️ No news found for {asset}, skipping...")
                continue
                
            total_score = 0
            count = 0
            
            # Analyze up to top 3 headlines
            for article in news[:3]:
                # This logic handles multiple Yahoo Finance data formats
                content = article.get('content', article)
                title = content.get('title') or article.get('title') or "No Title"
                
                analysis = engine.analyze_text(title)
                total_score += analysis['score']
                count += 1
            
            if count > 0:
                avg_score = total_score / count
                label = "Positive" if avg_score > 0.05 else "Negative" if avg_score < -0.05 else "Neutral"
                
                # Push results to your Supabase cloud database
                save_sentiment_to_cloud(asset, round(avg_score, 4), label)
            
        except Exception as e:
            print(f"❌ Error updating {asset}: {e}")
            
    print("\n✅ All assets updated in Supabase!")

if __name__ == "__main__":
    run_portfolio_update()