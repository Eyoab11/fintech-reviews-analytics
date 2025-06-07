from google_play_scraper import reviews
import pandas as pd
import time

# Define app IDs
app_ids = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}

all_reviews = []
for bank, app_id in app_ids.items():  # Fixed: changed 'apps' to 'app_ids'
    reviews_collected = 0
    token = None
    try:
        while reviews_collected < 400:
            result, token = reviews(
                app_id,
                lang="en",
                country="et",
                count=100,
                continuation_token=token
            )
            if not result:  # Handle empty results
                print(f"No more reviews for {bank}")
                break
            for review in result:
                all_reviews.append({
                    "review": review["content"] or "",  # Handle None values
                    "rating": review["score"],
                    "date": review["at"],
                    "bank": bank,
                    "source": "Google Play"
                })
            reviews_collected += len(result)
            print(f"Collected {reviews_collected} reviews for {bank}")
            time.sleep(1)  # Avoid rate limits
    except Exception as e:
        print(f"Error scraping {bank}: {e}")
    print(f"Total collected: {reviews_collected} reviews for {bank}")

# Save to CSV
df = pd.DataFrame(all_reviews)
df.to_csv("data/raw/reviews_raw.csv", index=False)
print("Saved reviews to data/raw/reviews_raw.csv")