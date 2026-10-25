#!/usr/bin/env python3
"""
fetch_toast_shorts_transcripts.py

Fetches transcripts for all 129 Toast YouTube Shorts from transcribeyoutube.com,
saving raw transcripts to raw-transcripts/toast/shorts/serial_XXX_<vid>.txt.
"""

import csv
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from curl_cffi import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CSV_PATH = os.path.join("sources", "youtube-lists", "toast-shorts.csv")
RAW_DIR = os.path.join("raw-transcripts", "toast", "shorts")
os.makedirs(RAW_DIR, exist_ok=True)

def fetch_single(row):
    serial = int(row["serial"])
    vid = row["video_id"]
    title = row["title"]
    url = row["url"]
    raw_path = os.path.join(RAW_DIR, f"serial_{serial:03d}_{vid}.txt")

    if os.path.exists(raw_path) and os.path.getsize(raw_path) > 50:
        return serial, "ALREADY_EXISTS", 0

    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = requests.post(
                "https://transcribeyoutube.com/api/transcript",
                json={"url": url},
                impersonate="chrome",
                timeout=30
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    snippets = data.get("transcript", [])
                    if snippets:
                        text = " ".join(item.get("text", "") for item in snippets)
                        text = re.sub(r"\s+", " ", text).strip()
                        with open(raw_path, "w", encoding="utf-8") as f:
                            f.write(f"Title: {title}\nURL: {url}\n\n{text}")
                        return serial, "SUCCESS", len(text.split())
                    else:
                        with open(raw_path, "w", encoding="utf-8") as f:
                            f.write(f"Title: {title}\nURL: {url}\n\n[NO TRANSCRIPT AVAILABLE]")
                        return serial, "EMPTY", 0
                else:
                    msg = data.get("message", "unknown error")
                    with open(raw_path, "w", encoding="utf-8") as f:
                        f.write(f"Title: {title}\nURL: {url}\n\n[NO TRANSCRIPT: {msg}]")
                    return serial, "NO_TRANSCRIPT", 0
            elif resp.status_code == 429:
                time.sleep(3.0 * (attempt + 1))
            else:
                time.sleep(1.5)
        except Exception as e:
            time.sleep(1.5)

    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\nURL: {url}\n\n[FETCH FAILED]")
    return serial, "FAILED", 0

def main():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total shorts to fetch: {len(rows)}")
    results = {}
    # Use max_workers=3 for polite throughput without triggering rate limits
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_row = {executor.submit(fetch_single, r): r for r in rows}
        for future in as_completed(future_to_row):
            serial, status, words = future.result()
            results[serial] = (status, words)
            print(f"Serial {serial:03d}: {status} ({words} words)")

    success_cnt = sum(1 for s, w in results.values() if s in ("SUCCESS", "ALREADY_EXISTS"))
    empty_cnt = sum(1 for s, w in results.values() if s in ("EMPTY", "NO_TRANSCRIPT"))
    failed_cnt = sum(1 for s, w in results.values() if s == "FAILED")
    print(f"\nFetch complete: {success_cnt} with text, {empty_cnt} empty/no transcript, {failed_cnt} failed.")

if __name__ == "__main__":
    main()
