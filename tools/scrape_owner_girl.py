import json
import subprocess
import sys
import os
import csv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def scrape_channel_tab(url, json_out_path, csv_out_path):
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
            data = json.loads(line)
            entries.append(data)
        except Exception as e:
            pass

    proc.wait()
    print(f"Found {len(entries)} items for {url}.")

    os.makedirs(os.path.dirname(json_out_path), exist_ok=True)
    with open(json_out_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f"Saved raw flat metadata to {json_out_path}")

    # Write CSV
    os.makedirs(os.path.dirname(csv_out_path), exist_ok=True)
    with open(csv_out_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["serial", "title", "url", "video_id", "processed"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for idx, entry in enumerate(entries, start=1):
            vid = entry.get("id") or entry.get("url")
            title = entry.get("title") or f"Video {idx}"
            full_url = f"https://www.youtube.com/watch?v={vid}"
            writer.writerow({
                "serial": f"{idx:03d}",
                "title": title,
                "url": full_url,
                "video_id": vid,
                "processed": "no"
            })
    print(f"Saved {len(entries)} rows to {csv_out_path}")

if __name__ == "__main__":
    scrape_channel_tab(
        "https://www.youtube.com/@makingdoughshow/shorts",
        "scratch/owner_girl_shorts_flat_info.json",
        "sources/youtube-lists/owner-girl-shorts.csv"
    )
    scrape_channel_tab(
        "https://www.youtube.com/@makingdoughshow/videos",
        "scratch/owner_girl_videos_flat_info.json",
        "sources/youtube-lists/owner-girl-videos.csv"
    )
