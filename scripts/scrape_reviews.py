from google_play_scraper import Sort, reviews_all
import pandas as pd
from tqdm import tqdm
from datetime import datetime

APPS = {
    "Touch n Go eWallet": "my.com.tngdigital.ewallet",
    "Boost": "my.myboost",
    "MAE by Maybank": "com.maybank2u.life",
    "GXBank": "my.com.gxbank",
    "Setel": "com.setel.mobile",
}

# Scrape both English and Malay reviews for full Malaysian coverage
LANGUAGES = ["en", "ms"]
COUNTRY = "my"

all_reviews = []

for app_name, app_id in tqdm(APPS.items(), desc="Apps"):
    for lang in LANGUAGES:
        try:
            print(f"\n→ Scraping {app_name} ({lang})...")
            result = reviews_all(
                app_id,
                sleep_milliseconds=100,   # be polite to Google
                lang=lang,
                country=COUNTRY,
                sort=Sort.NEWEST,
            )
            for r in result:
                r["app_name"] = app_name
                r["scraped_lang"] = lang
            all_reviews.extend(result)
            print(f"   got {len(result)} reviews")
        except Exception as e:
            print(f"   ⚠️ failed: {e}")

df = pd.DataFrame(all_reviews)

# Keep only what we need
keep_cols = ["app_name", "scraped_lang", "userName", "score", "content",
             "thumbsUpCount", "reviewCreatedVersion", "at", "replyContent", "repliedAt"]
df = df[[c for c in keep_cols if c in df.columns]]

# Save with timestamp
filename = f"reviews_raw_{datetime.now().strftime('%Y%m%d')}.csv"
df.to_csv(filename, index=False)

print(f"\n✅ Saved {len(df):,} reviews to {filename}")
print("\nReview count per app:")
print(df.groupby("app_name").size().sort_values(ascending=False))