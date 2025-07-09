import pandas as pd
import time
from textblob import TextBlob
import feedparser

# --- CONFIG ---
INPUT_META_PATH = '../data/full_retail_meta_dataset.csv'
OUTPUT_META_PATH = '../data/full_retail_meta_dataset.csv'

# ✅ Optional: known brand list for better matching
known_brands = [
    'amul', 'lays', 'maggi', 'tata', 'dove', 'colgate', 'nivea', 'classmate', 'reynolds',
    'amazonbasics', 'jk', 'borosil', 'cello', 'prestige', 'lifebuoy', 'dr trust',
    'revital', 'moov', 'bombay dyeing', 'trident', 'petzone', 'milton'
]

def extract_brand(product_name: str) -> str:
    product_name_lower = product_name.lower()
    for brand in known_brands:
        if brand in product_name_lower:
            return brand
    return product_name.split()[0].lower()

def fetch_google_news_sentiment(brand: str) -> float:
    try:
        feed = feedparser.parse(f'https://news.google.com/rss/search?q={brand}+product&hl=en-IN&gl=IN&ceid=IN:en')
        if not feed.entries:
            print(f"[⚠️ No news found] {brand}")
            return 0.1

        sentiments = []
        for entry in feed.entries[:15]:  # limit to top 15 results
            text = f"{entry.title} {entry.description}"
            polarity = TextBlob(text).sentiment.polarity
            sentiments.append(polarity)

        avg = round(sum(sentiments) / len(sentiments), 2) if sentiments else 0.1
        return avg
    except Exception as e:
        print(f"[❌ Error] {brand}: {e}")
        return 0.1

def generate_brand_reputation_score():
    df = pd.read_csv(INPUT_META_PATH)
    df['brand'] = df['product_name'].apply(extract_brand)

    print("🔍 Calculating brand reputation scores (Google News)...")
    brand_sentiment_map = {}
    for brand in df['brand'].unique():
        score = fetch_google_news_sentiment(brand)
        brand_sentiment_map[brand] = score
        print(f"✅ {brand}: raw sentiment = {score}")
        time.sleep(1)  # be polite to Google

    # Scale raw sentiment to 1–5
    sentiment_series = pd.Series(brand_sentiment_map)
    min_val, max_val = sentiment_series.min(), sentiment_series.max()
    if min_val == max_val:
        scaled = pd.Series(3.0, index=sentiment_series.index)
    else:
        scaled = 1 + 4 * (sentiment_series - min_val) / (max_val - min_val)

    df['brand_reputation_score'] = df['brand'].map(scaled.round(2))
    df.drop(columns=['brand'], inplace=True)

    df.to_csv(OUTPUT_META_PATH, index=False)
    print(f"\n✅ Brand reputation scores saved to: {OUTPUT_META_PATH}")

if __name__ == '__main__':
    generate_brand_reputation_score()
