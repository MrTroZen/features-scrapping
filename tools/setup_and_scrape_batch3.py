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

PROJECTS = [
    {
        "name": "Wilson F&B",
        "slug": "wilson-fb",
        "shorts_url": "https://www.youtube.com/@WilsonKLee/shorts",
        "videos_url": "https://www.youtube.com/@WilsonKLee/videos"
    },
    {
        "name": "Smart Pizza",
        "slug": "smart-pizza",
        "shorts_url": "https://www.youtube.com/@Smartpizzamarketing/shorts",
        "videos_url": "https://www.youtube.com/@Smartpizzamarketing/videos"
    },
    {
        "name": "Matt Plapp",
        "slug": "matt-plapp",
        "shorts_url": "https://www.youtube.com/@matt_plapp/shorts",
        "videos_url": "https://www.youtube.com/@matt_plapp/videos"
    }
]

def init_project_folders(slug):
    base_dir = os.path.join("knowledge", slug)
    short_dir = os.path.join(base_dir, f"{slug}-short-form")
    full_dir = os.path.join(base_dir, f"{slug}-full-form")

    for p in [short_dir, full_dir]:
        for cat in CATEGORIES:
            cat_path = os.path.join(p, cat)
            os.makedirs(cat_path, exist_ok=True)
            gitkeep = os.path.join(cat_path, ".gitkeep")
            if not os.path.exists(gitkeep):
                with open(gitkeep, "w", encoding="utf-8") as f:
                    f.write("")
    print(f"Initialized knowledge directories for {slug}.")

def scrape_tab(url, json_out, csv_out):
    print(f"Scraping {url} ...")
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

    print(f"  -> Found {len(entries)} items.")

    os.makedirs(os.path.dirname(json_out), exist_ok=True)
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    os.makedirs(os.path.dirname(csv_out), exist_ok=True)
    fieldnames = ["serial", "title", "url", "video_id", "processed"]
    with open(csv_out, "w", newline="", encoding="utf-8") as f:
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
    print(f"  -> Saved {len(entries)} catalog rows to {csv_out}")
    return len(entries)

def main():
    summary = {}
    for p in PROJECTS:
        slug = p["slug"]
        name = p["name"]
        print(f"\n==========================================")
        print(f"Setting up Project: {name} ({slug})")
        print(f"==========================================")
        
        init_project_folders(slug)
        
        shorts_json = os.path.join("scratch", f"{slug}_shorts_flat_info.json")
        shorts_csv = os.path.join("sources", "youtube-lists", f"{slug}-shorts.csv")
        s_count = scrape_tab(p["shorts_url"], shorts_json, shorts_csv)

        videos_json = os.path.join("scratch", f"{slug}_videos_flat_info.json")
        videos_csv = os.path.join("sources", "youtube-lists", f"{slug}-videos.csv")
        v_count = scrape_tab(p["videos_url"], videos_json, videos_csv)

        summary[name] = {"shorts": s_count, "videos": v_count}

    print("\n\n==========================================")
    print("ALL 3 PROJECTS INITIALIZED & SCRAPED:")
    print("==========================================")
    for name, counts in summary.items():
        print(f"  {name}: {counts['shorts']} Shorts | {counts['videos']} Long-Form Videos")

if __name__ == "__main__":
    main()
