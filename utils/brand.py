import time
import feedparser
from textblob import TextBlob

# ✅ Optional: known brand list for better matching
known_brands = [
    'amul', 'lays', 'maggi', 'tata', 'dove', 'colgate', 'nivea', 'classmate', 'reynolds',
    'amazonbasics', 'jk', 'borosil', 'cello', 'prestige', 'lifebuoy', 'dr trust',
    'revital', 'moov', 'bombay dyeing', 'trident', 'petzone', 'milton'
]

def extract_brand(product_name: str) -> str:
    """
    Extract brand name from product_name using known brand list.
    """
    product_name_lower = product_name.lower()
    for brand in known_brands:
        if brand in product_name_lower:
            return brand
    return product_name.split()[0].lower()

def fetch_google_news_sentiment(brand: str) -> float:
    """
    Fetch sentiment polarity for a brand from Google News RSS feed.
    """
    try:
        feed = feedparser.parse(
            f'https://news.google.com/rss/search?q={brand}+product&hl=en-IN&gl=IN&ceid=IN:en'
        )
        if not feed.entries:
            print(f"[⚠️ No news found] {brand}")
            return 0.1

        sentiments = []
        for entry in feed.entries[:15]:
            text = f"{entry.title} {entry.description}"
            polarity = TextBlob(text).sentiment.polarity
            sentiments.append(polarity)

        avg = round(sum(sentiments) / len(sentiments), 2) if sentiments else 0.1
        return avg
    except Exception as e:
        print(f"[❌ Error] {brand}: {e}")
        return 0.1

def get_brand_reputation_score(product_name: str) -> float:
    """
    Utility function for dynamic use in /new_product route.
    Extract brand and fetch reputation score.
    """
    brand = extract_brand(product_name)
    sentiment = fetch_google_news_sentiment(brand)
    scaled_score = round(1 + 4 * ((sentiment + 1) / 2), 2)  # map -1 to +1 --> 1 to 5
    return min(max(scaled_score, 1.0), 5.0)
