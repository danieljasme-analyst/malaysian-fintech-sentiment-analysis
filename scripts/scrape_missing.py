from google_play_scraper import Sort, reviews_all
import pandas as pd
from datetime import datetime

MISSING_APPS = {
    "Boost": "my.com.myboost",
    "GXBank": "my.com.gxbank.app",
}

LANGUAGES = ["en", "ms"]
COUNTRY = "my"

new_reviews = []

for app_name, app_id in MISSING_APPS.items():
    for lang in LANGUAGES:
        try:
            print(f"→ Scraping {app_name} ({lang})...")
            result = reviews_all(
                app_id,
                sleep_milliseconds=100,
                lang=lang,
                country=COUNTRY,
                sort=Sort.NEWEST,
            )
            for r in result:
                r["app_name"] = app_name
                r["scraped_lang"] = lang
            new_reviews.extend(result)
            print(f"   got {len(result)} reviews")
        except Exception as e:
            print(f"   ⚠️ failed: {e}")

new_df = pd.DataFrame(new_reviews)
keep_cols = ["app_name", "scraped_lang", "userName", "score", "content",
             "thumbsUpCount", "reviewCreatedVersion", "at", "replyContent", "repliedAt"]
new_df = new_df[[c for c in keep_cols if c in new_df.columns]]

# Load the original CSV and append
existing_df = pd.read_csv("reviews_raw_20260605.csv")
combined = pd.concat([existing_df, new_df], ignore_index=True)

# Save as the final dataset
filename = f"reviews_raw_combined_{datetime.now().strftime('%Y%m%d')}.csv"
combined.to_csv(filename, index=False)

print(f"\n✅ Total combined: {len(combined):,} reviews → {filename}")
print("\nReview count per app:")
print(combined.groupby("app_name").size().sort_values(ascending=False))