import yfinance as yf
from sentiment_engine import MarketSentiment # Importing your class!

def get_market_mood(ticker_symbol):
    engine = MarketSentiment()
    ticker = yf.Ticker(ticker_symbol)
    news = ticker.news
    
    total_score = 0
    count = 0
    
    print(f"\n--- Analyzing Mood for {ticker_symbol} ---")
    
    for article in news[:5]: # Analyze the top 5 latest headlines
        # Using the fix we found earlier for the title location
        content = article.get('content', article)
        title = content.get('title', 'No Title')
        
        analysis = engine.analyze_text(title)
        print(f"Title: {title[:60]}... | Result: {analysis['label']} ({analysis['score']})")
        
        total_score += analysis['score']
        count += 1
    
    if count > 0:
        avg_score = total_score / count
        # 4th Year Logic: Converting the score to a "Safety Level"
        if avg_score > 0.1: safety = "🟢 SAFE (Positive Mood)"
        elif avg_score < -0.1: safety = "🔴 RISKY (Negative Mood)"
        else: safety = "🟡 NEUTRAL"
        
        print(f"\nOVERALL MOOD: {safety} (Score: {round(avg_score, 4)})")
    else:
        print("No news found to analyze.")

if __name__ == "__main__":
    # Test it with a mix of Indian Tech and Crypto
    get_market_mood("TCS.NS")
    get_market_mood("BTC-USD")