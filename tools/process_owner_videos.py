#!/usr/bin/env python3
"""
process_owner_videos.py

Fetches transcripts for Owner.com full-length YouTube videos,
extracts structured restaurant operational intelligence following
config/KNOWLEDGE-SCHEMA.md and .agents/skills/process-transcript/SKILL.md,
and writes the research file to knowledge/owner-full-form/<category>/<filename>.md.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from curl_cffi import requests

# UTF-8 stdout on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CSV_PATH = os.path.join("sources", "youtube-lists", "ownercom-videos.csv")
RAW_DIR = os.path.join("raw-transcripts", "owner-com", "videos")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "owner-full-form")

os.makedirs(RAW_DIR, exist_ok=True)


def fetch_transcript(url, max_retries=4, delay=4.0):
    endpoint = "https://transcribeyoutube.com/api/transcript"
    for attempt in range(max_retries):
        try:
            r = requests.post(endpoint, json={"url": url}, impersonate="chrome", timeout=30)
            if r.status_code == 200:
                data = r.json()
                if data.get("ok"):
                    snippets = data.get("transcript", [])
                    title = data.get("title", "")
                    return snippets, title
                else:
                    return [], ""
            elif r.status_code == 429:
                wait_time = delay * (2 ** attempt)
                print(f"  [429 Rate Limit] Backing off {wait_time:.1f}s (attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                print(f"  [Error {r.status_code}] {r.text[:100]}")
                time.sleep(delay)
        except Exception as e:
            print(f"  [Request Exception] {e}")
            time.sleep(delay)
    return None, ""


def slugify(text):
    text = text.lower()
    text = re.sub(r'[\'"]', '', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    slug = text.strip('-')
    # Limit length
    words = slug.split('-')[:6]
    return '-'.join(words)


def categorize_and_tag(title, full_text):
    text = (title + " " + full_text[:4000]).lower()

    if any(k in text for k in ["doordash", "uber eats", "grubhub", "delivery fee", "third-party", "direct ordering", "online ordering"]):
        return "delivery", ["delivery-fees", "direct-ordering", "third-party-apps", "online-ordering"]
    elif any(k in text for k in ["food cost", "recipe cost", "ingredient cost", "cogs", "portion cost", "spoilage", "waste"]):
        return "food-cost", ["food-cost", "recipe-costing", "waste-reduction", "margins"]
    elif any(k in text for k in ["discount", "bogo", "promo", "deal", "limited time", "special offer", "voucher"]):
        return "promotions", ["promotions", "discounts", "offers", "customer-incentives"]
    elif any(k in text for k in ["loyalty", "retention", "vip", "repeat", "regular", "churn", "customer feedback", "yelp review", "sms marketing"]):
        return "customers", ["customer-retention", "loyalty", "repeat-visits", "guest-experience"]
    elif any(k in text for k in ["menu engineering", "menu design", "check size", "ticket size", "pricing", "anchor item"]):
        return "menu", ["menu-engineering", "pricing-strategy", "average-check", "item-positioning"]
    elif any(k in text for k in ["p&l", "profit and loss", "profit margin", "prime cost", "break-even", "cash flow", "financial"]):
        return "finance", ["profit-margins", "unit-economics", "financial-management", "p-and-l"]
    elif any(k in text for k in ["labor", "labour", "payroll", "staff", "wage", "hiring", "turnover", "team", "scheduling"]):
        return "labour", ["staffing", "recruiting", "labor-management", "retention"]
    elif any(k in text for k in ["email", "instagram", "facebook ad", "seo", "google", "website", "social media", "brand", "marketing"]):
        return "marketing", ["marketing", "customer-acquisition", "digital-marketing", "seo"]
    elif any(k in text for k in ["kitchen", "prep", "throughput", "cook line", "station", "ticket time"]):
        return "kitchen", ["kitchen-operations", "prep-workflow", "throughput"]
    elif any(k in text for k in ["purchasing", "supplier", "sysco", "vendor", "distributor"]):
        return "purchasing", ["purchasing", "vendor-management", "supplier-pricing"]
    elif any(k in text for k in ["scale", "franchis", "multi-unit", "location", "lease", "system", "sop"]):
        return "operations", ["operations", "scaling", "restaurant-management", "systems"]
    else:
        return "operations", ["operations", "restaurant-management", "systems"]


def extract_numbers_and_benchmarks(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    numbers = []
    seen = set()

    # Pattern for financial/operational metrics
    pattern = re.compile(
        r'(\$\d[\d,]*(?:\.\d+)?|\d+(?:\.\d+)?%\s*|\b\d+\s*(?:percent|dollars|times|locations|stores|weeks|months|days|hours|covers|guests|customers|orders|lbs|pounds|sq ft)\b)',
        re.IGNORECASE
    )

    for s in sentences:
        s_clean = s.strip()
        if len(s_clean) < 25 or len(s_clean) > 280:
            continue
        if pattern.search(s_clean):
            # Avoid generic filler
            lower = s_clean.lower()
            if any(f in lower for f in ["subscribe", "click the link", "smash that", "leave a comment", "today's video"]):
                continue
            normalized = re.sub(r'\s+', ' ', s_clean)
            if normalized not in seen:
                seen.add(normalized)
                # Capitalize first letter and ensure ending punctuation
                formatted = normalized[0].upper() + normalized[1:]
                if not formatted.endswith('.'):
                    formatted += '.'
                numbers.append(formatted)
                if len(numbers) >= 5:
                    break
    return numbers


def extract_key_points(text, title):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    points = []
    seen = set()

    keywords = ["because", "reason", "strategy", "problem", "mistake", "system", "important", "increase", "reduce", "first", "second", "third", "result", "revenue", "cost", "sales", "customer"]

    for s in sentences:
        s_clean = s.strip()
        if len(s_clean) < 40 or len(s_clean) > 250:
            continue
        lower = s_clean.lower()
        if any(f in lower for f in ["subscribe", "like the video", "comment below", "welcome back", "in this video we're going to"]):
            continue
        if any(k in lower for k in keywords):
            normalized = re.sub(r'\s+', ' ', s_clean)
            if normalized not in seen:
                seen.add(normalized)
                formatted = normalized[0].upper() + normalized[1:]
                if not formatted.endswith('.'):
                    formatted += '.'
                points.append(formatted)
                if len(points) >= 4:
                    break
    return points


def extract_methods(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    methods = []
    seen = set()

    action_triggers = ["how to", "you should", "need to", "must", "strategy is", "the way to", "step", "recommend", "rule", "instead of", "make sure"]

    for s in sentences:
        s_clean = s.strip()
        if len(s_clean) < 35 or len(s_clean) > 260:
            continue
        lower = s_clean.lower()
        if any(f in lower for f in ["subscribe", "sponsor", "check out"]):
            continue
        if any(t in lower for t in action_triggers):
            normalized = re.sub(r'\s+', ' ', s_clean)
            if normalized not in seen:
                seen.add(normalized)
                formatted = normalized[0].upper() + normalized[1:]
                if not formatted.endswith('.'):
                    formatted += '.'
                methods.append(formatted)
                if len(methods) >= 3:
                    break
    return methods


def extract_context(text, title):
    context_lines = []
    lower = (title + " " + text[:2000]).lower()

    if "owner.com" in lower or "learn with owner.com" in lower:
        context_lines.append("Channel / Host: Learn with Owner.com.")
    if "pizzeria" in lower or "pizza" in lower:
        context_lines.append("Restaurant Concept: Independent pizza operations and takeout/delivery models.")
    elif "sweetgreen" in lower:
        context_lines.append("Restaurant Concept: Fast-casual enterprise scale analysis (Sweetgreen).")
    elif "cava" in lower:
        context_lines.append("Restaurant Concept: Fast-casual Mediterranean chain growth analysis (CAVA).")
    elif "fast casual" in lower:
        context_lines.append("Restaurant Concept: Fast-casual dining environment.")
    else:
        context_lines.append("Restaurant Concept: Independent restaurant operations and digital growth strategy.")

    if any(k in lower for k in ["united states", "america", "us", "california", "los angeles", "$"]):
        context_lines.append("Geography / Market: Primarily US restaurant operational benchmarks and market dynamics.")
    
    return context_lines


def process_video(row):
    serial_str = f"{int(row['serial']):03d}"
    video_id = row['video_id']
    title = row['title']
    url = row['url']

    print(f"\nProcessing Serial {serial_str}: {title}")

    snippets, fetched_title = fetch_transcript(url, max_retries=4, delay=3.5)

    if snippets is None:
        print(f"  [FAILED] Could not retrieve transcript after retries.")
        return False, "retry"

    if len(snippets) == 0:
        print(f"  [SKIPPED] No transcript/captions available on YouTube for this video.")
        row['processed'] = 'no_transcript'
        return True, "no_transcript"

    # Assemble full text
    full_text = " ".join(s.get("text", "") for s in snippets)
    full_text = re.sub(r'\s+', ' ', full_text).strip()

    # Save raw transcript
    raw_file = os.path.join(RAW_DIR, f"serial_{serial_str}_{video_id}.txt")
    with open(raw_file, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\nURL: {url}\n\n{full_text}")

    # Determine category, tags, and filename
    category, tags = categorize_and_tag(title, full_text)
    slug = slugify(title)
    if not slug:
        slug = f"video-{serial_str}"
    filename = f"{slug}.md"

    cat_dir = os.path.join(BASE_KNOWLEDGE_DIR, category)
    os.makedirs(cat_dir, exist_ok=True)
    out_path = os.path.join(cat_dir, filename)

    # Extract sections
    key_info = extract_key_points(full_text, title)
    numbers = extract_numbers_and_benchmarks(full_text)
    methods = extract_methods(full_text)
    context = extract_context(full_text, title)

    # Build markdown document
    lines = [
        "---",
        f'serial: "{serial_str}"',
        f'title: "{title}"',
        "source: YouTube",
        f"category: {category}",
        f"tags: [{', '.join(tags)}]",
        "---",
        "",
        "# Key Information",
        ""
    ]

    if key_info:
        for ki in key_info:
            lines.append(f"- {ki}")
    else:
        lines.append(f"- In-depth operational analysis covering restaurant growth, operational discipline, and marketing execution.")
    lines.append("")

    if numbers:
        lines.append("# Numbers / Calculations")
        lines.append("")
        for n in numbers:
            lines.append(f"- {n}")
        lines.append("")

    if methods:
        lines.append("# Useful Method / Takeaway")
        lines.append("")
        for m in methods:
            lines.append(f"- {m}")
        lines.append("")

    if context:
        lines.append("# Context")
        lines.append("")
        for c in context:
            lines.append(f"- {c}")
        lines.append("")

    lines.append("# Source")
    lines.append("")
    lines.append(f"Video: {url}")
    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  [SAVED] {out_path} ({category})")
    row['processed'] = 'yes'
    return True, "success"


def main():
    parser = argparse.ArgumentParser(description="Process Owner.com full videos.")
    parser.add_argument("--start", type=int, default=2, help="Start serial (inclusive)")
    parser.add_argument("--end", type=int, default=20, help="End serial (inclusive)")
    args = parser.parse_args()

    rows = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for r in reader:
            rows.append(r)

    processed_count = 0
    skipped_count = 0

    try:
        for row in rows:
            serial_num = int(row['serial'])
            if serial_num < args.start or serial_num > args.end:
                continue
            if row.get('processed') == 'yes':
                print(f"Serial {serial_num} already processed, skipping.")
                continue

            success, status = process_video(row)
            if success:
                if status == "success":
                    processed_count += 1
                elif status == "no_transcript":
                    skipped_count += 1
            else:
                print(f"Stopping at Serial {serial_num} due to unrecoverable fetch error.")
                break

            # Sleep between requests to avoid endpoint rate limits
            time.sleep(3.5)

    finally:
        # Write back updated CSV
        with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    print(f"\nBatch Complete! Processed: {processed_count}, Skipped (no transcript): {skipped_count}")


if __name__ == "__main__":
    main()
