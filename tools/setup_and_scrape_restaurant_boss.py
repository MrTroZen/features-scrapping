import csv
import json
import os
import subprocess
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CATEGORIES = [
    "customers", "delivery", "finance", "food-cost", "forecasting",
    "inventory", "kitchen", "labour", "marketing", "menu",
    "operations", "other", "payments", "promotions", "purchasing", "social"
]

BASE_DIR = os.path.join("knowledge", "restaurant-boss")
SHORT_DIR = os.path.join(BASE_DIR, "restaurant-boss-short-form")
FULL_DIR = os.path.join(BASE_DIR, "restaurant-boss-full-form")

# 1. Setup folder structure
for parent_dir in [SHORT_DIR, FULL_DIR]:
    for cat in CATEGORIES:
        cat_path = os.path.join(parent_dir, cat)
        os.makedirs(cat_path, exist_ok=True)
        gitkeep = os.path.join(cat_path, ".gitkeep")
        if not os.path.exists(gitkeep):
            with open(gitkeep, "w", encoding="utf-8") as f:
                f.write("")

print(f"Created knowledge structure in {BASE_DIR} for short-form and full-form with all 16 categories.")

# 2. Function to scrape a YouTube tab using yt-dlp
def scrape_youtube_tab(url, json_out_path, csv_out_path):
    print(f"\nScraping {url} ...")
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-json",
        "--ignore-errors",
        url
    ]
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    entries = []
    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except Exception:
            pass
    proc.wait()

    print(f"Scraped {len(entries)} items from {url}.")

    os.makedirs(os.path.dirname(json_out_path), exist_ok=True)
    with open(json_out_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f"Saved metadata to {json_out_path}")

    os.makedirs(os.path.dirname(csv_out_path), exist_ok=True)
    fieldnames = ["serial", "title", "url", "video_id", "processed"]
    with open(csv_out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for idx, item in enumerate(entries, start=1):
            vid = item.get("id") or item.get("url")
            title = item.get("title") or f"Video {idx}"
            full_url = f"https://www.youtube.com/watch?v={vid}"
            writer.writerow({
                "serial": f"{idx:03d}",
                "title": title,
                "url": full_url,
                "video_id": vid,
                "processed": "no"
            })
    print(f"Saved {len(entries)} catalog rows to {csv_out_path}")

if __name__ == "__main__":
    scrape_youtube_tab(
        "https://www.youtube.com/@Therestaurantboss/shorts",
        "scratch/restaurant_boss_shorts_flat_info.json",
        "sources/youtube-lists/restaurant-boss-shorts.csv"
    )
    scrape_youtube_tab(
        "https://www.youtube.com/@Therestaurantboss/videos",
        "scratch/restaurant_boss_videos_flat_info.json",
        "sources/youtube-lists/restaurant-boss-videos.csv"
    )
