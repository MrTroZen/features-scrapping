#!/usr/bin/env python3
"""
collect-youtube-videos.py

Collects every public YouTube long-form/full video from a channel's Videos tab,
orders them from oldest to newest, and saves/updates an indexed CSV list.
"""

import argparse
import csv
import os
import sys
import yt_dlp

# Ensure standard output supports UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class SilentLogger:
    def debug(self, msg):
        pass

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Collect public YouTube full videos from a channel's Videos tab."
    )
    parser.add_argument(
        "url",
        help="YouTube channel Videos URL (e.g. https://www.youtube.com/@owner-com/videos)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Path to output CSV (default: sources/youtube-lists/ownercom-videos.csv for Owner.com)",
    )
    return parser.parse_args()


def determine_default_output(url, channel_title):
    lower_url = url.lower()
    lower_title = (channel_title or "").lower()
    if "owner" in lower_url or "owner" in lower_title:
        return os.path.join("sources", "youtube-lists", "ownercom-videos.csv")

    # Fallback to slug from URL or title
    slug = "channel"
    if "@" in url:
        slug = url.split("@")[-1].split("/")[0].strip()
    elif channel_title:
        slug = "".join(c if c.isalnum() else "-" for c in channel_title).strip("-").lower()
    return os.path.join("sources", "youtube-lists", f"{slug}-videos.csv")


def fetch_channel_videos(channel_url):
    url = channel_url.strip()
    if not url.endswith("/videos"):
        url = url.rstrip("/") + "/videos"

    candidates = [url]
    # Handle common alias where @ownercom is passed for Owner.com (actual handle: @owner-com)
    if "@ownercom" in url and "@owner-com" not in url:
        candidates.append(url.replace("@ownercom", "@owner-com"))
    elif "@owner-com" in url and "@ownercom" not in url:
        candidates.append(url.replace("@owner-com", "@ownercom"))

    ydl_opts = {
        "extract_flat": "in_playlist",
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
        "logger": SilentLogger(),
    }

    last_error = None
    for candidate in candidates:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(candidate, download=False)
                if info and info.get("entries"):
                    return info, candidate
        except Exception as err:
            last_error = err
            continue

    if last_error:
        raise last_error
    raise RuntimeError(f"Could not retrieve videos from {channel_url}")


def main():
    args = parse_arguments()
    input_url = args.url

    # Retrieve channel Videos metadata via yt-dlp
    info, resolved_url = fetch_channel_videos(input_url)

    channel_name = (
        info.get("channel")
        or info.get("uploader")
        or info.get("title", "")
    )
    if "owner" in channel_name.lower() or "owner" in input_url.lower():
        channel_display = "Owner.com"
    else:
        channel_display = channel_name.replace(" - Videos", "").strip() or "Unknown Channel"

    # 1. Count all unique video IDs retrieved
    raw_entries = info.get("entries", [])
    valid_entries = []
    seen_ids = set()
    for entry in raw_entries:
        if not entry:
            continue
        vid = entry.get("id")
        if vid and vid not in seen_ids:
            seen_ids.add(vid)
            valid_entries.append(entry)

    unique_ids_count = len(valid_entries)

    # 2. Check if yt-dlp exposes reported playlist / channel item count
    reported_count = info.get("playlist_count") or info.get("n_entries")
    is_incomplete = bool(reported_count is not None and unique_ids_count < reported_count)

    # YouTube Videos tab lists items from newest to oldest.
    # We reverse them so the list is strictly ordered OLDEST -> NEWEST.
    valid_entries.reverse()

    # Determine output path
    output_path = args.output
    if not output_path:
        output_path = determine_default_output(input_url, channel_name)

    # 4 & 5. Preserve existing rows and merge by video_id without deleting previously collected rows
    existing_records = {}
    existing_ids_order = []
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                vid = row.get("video_id")
                if vid and vid not in existing_records:
                    existing_records[vid] = row
                    existing_ids_order.append(vid)

    new_entries = [e for e in valid_entries if e["id"] not in existing_records]
    already_known = [e for e in valid_entries if e["id"] in existing_records]

    merged_list = []
    merged_ids = set()

    # If existing records exist:
    # - Preserve existing valid rows in established chronological order
    # - Append newly discovered Videos (newer uploads) in chronological order
    if existing_ids_order:
        for vid in existing_ids_order:
            prev = existing_records[vid]
            curr_entry = next((e for e in valid_entries if e["id"] == vid), None)
            title = (curr_entry.get("title") if curr_entry else None) or prev.get("title", "")
            merged_ids.add(vid)
            merged_list.append({
                "video_id": vid,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={vid}",
                "processed": prev.get("processed", "no"),
            })
        for item in new_entries:
            vid = item["id"]
            if vid not in merged_ids:
                merged_ids.add(vid)
                merged_list.append({
                    "video_id": vid,
                    "title": item.get("title", ""),
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "processed": "no",
                })
    else:
        for item in valid_entries:
            vid = item["id"]
            if vid not in merged_ids:
                merged_ids.add(vid)
                merged_list.append({
                    "video_id": vid,
                    "title": item.get("title", ""),
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "processed": "no",
                })

    # 7. Rebuild serial numbers sequentially starting at 1
    for idx, row in enumerate(merged_list, start=1):
        row["serial"] = idx

    # Save to CSV (never split even if containing thousands of rows)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    fieldnames = ["serial", "title", "url", "video_id", "processed"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in merged_list:
            writer.writerow({k: row[k] for k in fieldnames})

    # Normalized relative path for display
    rel_path = os.path.relpath(output_path, os.getcwd()).replace("\\", "/")

    # Print results
    print("Channel:")
    print(channel_display)
    if is_incomplete:
        print("Extraction status: potentially incomplete")
        print()
        print("Expected/reported:")
        print(reported_count)
        print()
        print("Unique Videos retrieved:")
        print(unique_ids_count)
    else:
        print("Extraction status: complete")
        print()
        print("Expected/reported:")
        print(reported_count if reported_count is not None else unique_ids_count)
        print()
        print("Unique Videos retrieved:")
        print(unique_ids_count)

    print()
    print("Videos found:")
    print(unique_ids_count)
    print("New Videos added:")
    print(len(new_entries))
    print("Already known:")
    print(len(already_known))
    print("Order:")
    print("oldest → newest")
    print("Saved:")
    print(rel_path)


if __name__ == "__main__":
    main()
