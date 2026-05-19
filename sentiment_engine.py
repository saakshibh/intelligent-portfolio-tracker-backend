import requests
import xml.etree.ElementTree as ET
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

class MarketSentiment:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def get_ticker_sentiment(self, ticker):
        print(f"📡 Fetching Live News (Deep Search) for: {ticker}")
        try:
            search_query = ticker.replace(".NS", "") + " stock news"
            url = f"https://news.google.com/rss/search?q={search_query}&hl=en-IN&gl=IN&ceid=IN:en"
            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return 0.05, []
            
            root = ET.fromstring(response.content)
            # INCREASED DEPTH: Grabbing top 10 news items instead of 5
            items = root.findall('.//item')[:10] 
            
            news_snippets = []
            scores = []
            
            for item in items:
                title = item.find('title').text
                # Extract the direct link to the news article
                link = item.find('link').text if item.find('link') is not None else "#"
                source = item.find('source').text if item.find('source') is not None else "Financial News"
                
                score = self.sia.polarity_scores(title)['compound']
                scores.append(score)
                
                news_snippets.append({
                    "title": title,
                    "source": source,
                    "link": link, # Added to JSON structure
                    "sentiment": "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"
                })
            
            avg_score = sum(scores) / len(scores) if scores else 0.03
            return round(avg_score, 2), news_snippets

        except Exception as e:
            print(f"⚠️ News Extraction failed: {e}")
            return 0.01, []

def get_sentiment(ticker):
    return MarketSentiment().get_ticker_sentiment(ticker)