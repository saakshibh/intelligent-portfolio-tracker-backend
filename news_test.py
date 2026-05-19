import yfinance as yf

def fetch_news_test():
    ticker = yf.Ticker("TCS.NS")
    news = ticker.news
    
    print(f"--- Latest News for TCS.NS ---")
    
    for article in news[:3]:
        # NEW LOGIC: Check if 'title' is inside a 'content' folder
        if 'content' in article:
            title = article['content'].get('title', 'No Title Found')
            link = article['content'].get('canonicalUrl', {}).get('url', 'No Link Found')
        else:
            # Fallback for the old format
            title = article.get('title', 'No Title Found')
            link = article.get('link', 'No Link Found')
            
        print(f"Title: {title}")
        print(f"Link: {link}")
        print("-" * 20)

if __name__ == "__main__":
    fetch_news_test()