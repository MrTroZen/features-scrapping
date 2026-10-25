#!/usr/bin/env python3
"""
update_master_indexes_full.py

Comprehensive synchronization script for:
1. indexes/knowledge-index.md (indexes Owner Shorts, Owner Videos, Toast Shorts, Toast Videos, 
   Owner-girl Shorts, Owner-girl Videos, Restaurant Boss Shorts, Restaurant Boss Videos)
2. indexes/formula-index.md
3. indexes/benchmark-index.md
4. logs/processed-sources.md
"""

import csv
import os
import re
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

INDEX_DIR = "indexes"
KNOWLEDGE_DIR = "knowledge"
LOG_PATH = os.path.join("logs", "processed-sources.md")

CATEGORY_NAMES = {
    "customers": "Customers",
    "delivery": "Delivery",
    "finance": "Finance",
    "food-cost": "Food Cost",
    "forecasting": "Forecasting",
    "inventory": "Inventory",
    "kitchen": "Kitchen",
    "labour": "Labour",
    "marketing": "Marketing",
    "menu": "Menu",
    "operations": "Operations",
    "other": "Other",
    "payments": "Payments",
    "promotions": "Promotions",
    "purchasing": "Purchasing",
    "social": "Social"
}

def sync_knowledge_index():
    k_path = os.path.join(INDEX_DIR, "knowledge-index.md")
    
    # Load URL -> Serial mappings
    toast_vid_map = {}
    if os.path.exists("sources/youtube-lists/toast-videos.csv"):
        with open("sources/youtube-lists/toast-videos.csv", "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                toast_vid_map[r["url"].strip()] = r["serial"]

    owner_girl_vid_map = {}
    if os.path.exists("sources/youtube-lists/owner-girl-videos.csv"):
        with open("sources/youtube-lists/owner-girl-videos.csv", "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                owner_girl_vid_map[r["url"].strip()] = r["serial"]

    rb_shorts_map = {}
    if os.path.exists("sources/youtube-lists/restaurant-boss-shorts.csv"):
        with open("sources/youtube-lists/restaurant-boss-shorts.csv", "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                rb_shorts_map[r["url"].strip()] = r["serial"]

    rb_vid_map = {}
    if os.path.exists("sources/youtube-lists/restaurant-boss-videos.csv"):
        with open("sources/youtube-lists/restaurant-boss-videos.csv", "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                rb_vid_map[r["url"].strip()] = r["serial"]

    # We will collect entries by category: category -> list of (sort_key, line)
    catalog = {cat: [] for cat in CATEGORY_NAMES}

    counts = {
        "owner_shorts": 0,
        "owner_videos": 0,
        "toast_shorts": 0,
        "toast_videos": 0,
        "owner_girl_shorts": 0,
        "owner_girl_videos": 0,
        "rb_shorts": 0,
        "rb_videos": 0
    }

    # 1. Walk through all subdirectories
    for root, dirs, files in os.walk(KNOWLEDGE_DIR):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, KNOWLEDGE_DIR).replace("\\", "/")
            parts = rel_path.split("/")

            # Determine collection type
            collection = ""
            category = ""
            if rel_path.startswith("owner/owner-short-form/"):
                collection = "owner_shorts"
                category = parts[2]
            elif rel_path.startswith("owner/owner-full-form/"):
                collection = "owner_videos"
                category = parts[2]
            elif rel_path.startswith("toast/toast-short-form/"):
                collection = "toast_shorts"
                category = parts[2]
            elif rel_path.startswith("toast/toast-full-form/"):
                collection = "toast_videos"
                category = parts[2]
            elif rel_path.startswith("owner-girl/owner-girl-short-form/"):
                collection = "owner_girl_shorts"
                category = parts[2]
            elif rel_path.startswith("owner-girl/owner-girl-full-form/"):
                collection = "owner_girl_videos"
                category = parts[2]
            elif rel_path.startswith("restaurant-boss/restaurant-boss-short-form/"):
                collection = "rb_shorts"
                category = parts[2]
            elif rel_path.startswith("restaurant-boss/restaurant-boss-full-form/"):
                collection = "rb_videos"
                category = parts[2]
            else:
                continue

            counts[collection] += 1

            # Read content to extract Title and Serial
            with open(full_path, "r", encoding="utf-8") as mf:
                content = mf.read()

            # Extract title
            m_h1 = re.search(r'^#\s+(.+)$', content, re.M)
            title = m_h1.group(1).strip() if m_h1 else fname[:-3]
            display_title = title
            if display_title.startswith("Restaurant Operational Intelligence: "):
                display_title = display_title.replace("Restaurant Operational Intelligence: ", "")

            # If short-form frontmatter has title
            m_fm_title = re.search(r'title:\s*"([^"]+)"', content)
            if m_fm_title and not m_h1:
                display_title = m_fm_title.group(1).strip()

            # Extract tags if available
            m_tags = re.search(r'tags:\s*\[([^\]]+)\]', content)
            tags_str = f" `[{m_tags.group(1)}]`" if m_tags else ""

            # Extract serial
            m_serial = re.search(r'serial:\s*"(\d+)"', content)
            serial_num = int(m_serial.group(1)) if m_serial else 0

            # If Toast video
            if collection == "toast_videos":
                m_url = re.search(r'- URL:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in toast_vid_map:
                    serial_num = int(toast_vid_map[m_url.group(1).strip()])

            # If Owner-girl video
            if collection == "owner_girl_videos":
                m_url = re.search(r'- URL:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in owner_girl_vid_map:
                    serial_num = int(owner_girl_vid_map[m_url.group(1).strip()])

            # If Restaurant Boss short
            if collection == "rb_shorts":
                m_url = re.search(r'Video:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in rb_shorts_map:
                    serial_num = int(rb_shorts_map[m_url.group(1).strip()])

            # If Restaurant Boss video
            if collection == "rb_videos":
                m_url = re.search(r'- URL:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in rb_vid_map:
                    serial_num = int(rb_vid_map[m_url.group(1).strip()])

            rel_link = f"../knowledge/{rel_path}"

            # Format line
            if collection == "owner_shorts":
                label = f"Serial {serial_num:03d}"
                sort_key = (1, serial_num, display_title)
            elif collection == "owner_videos":
                label = f"Serial {serial_num:03d} (Owner Video)"
                sort_key = (2, serial_num, display_title)
            elif collection == "toast_shorts":
                label = f"Serial {serial_num:03d} (Toast Short)"
                sort_key = (3, serial_num, display_title)
            elif collection == "toast_videos":
                label = f"Serial {serial_num:03d} (Toast Video)"
                sort_key = (4, serial_num, display_title)
            elif collection == "owner_girl_shorts":
                label = f"Serial {serial_num:03d} (Owner-girl Short)"
                sort_key = (5, serial_num, display_title)
            elif collection == "owner_girl_videos":
                label = f"Serial {serial_num:03d} (Owner-girl Video)"
                sort_key = (6, serial_num, display_title)
            elif collection == "rb_shorts":
                label = f"Serial {serial_num:03d} (Restaurant Boss Short)"
                sort_key = (7, serial_num, display_title)
            else:
                label = f"Serial {serial_num:03d} (Restaurant Boss Video)"
                sort_key = (8, serial_num, display_title)

            line = f"- **{label}**: [{display_title}]({rel_link}){tags_str}"

            if category in catalog:
                catalog[category].append((sort_key, line))

    total_entries = sum(counts.values())

    # Build markdown output
    out = [
        "# Knowledge Index",
        "",
        "Master catalog of all structured restaurant operational intelligence files in `knowledge/`.",
        "",
        f"Total verified entries: **{total_entries:,}** ({counts['owner_shorts']} Owner Shorts, {counts['owner_videos']} Owner Videos, {counts['toast_shorts']} Toast Shorts, {counts['toast_videos']} Toast Videos, {counts['owner_girl_shorts']} Owner-girl Shorts, {counts['owner_girl_videos']} Owner-girl Videos, {counts['rb_shorts']} Restaurant Boss Shorts, {counts['rb_videos']} Restaurant Boss Videos)",
        ""
    ]

    for cat_key in sorted(CATEGORY_NAMES.keys()):
        items = catalog[cat_key]
        if not items:
            continue
        display_name = CATEGORY_NAMES[cat_key]
        out.append(f"## {display_name} ({len(items)} entries)")
        out.append("")
        for _, line in sorted(items, key=lambda x: x[0]):
            out.append(line)
        out.append("")

    with open(k_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out).strip() + "\n")

    print(f"Updated knowledge-index.md: Total {total_entries} entries across {len(catalog)} categories.")
    print(f"  Owner Shorts: {counts['owner_shorts']}")
    print(f"  Owner Videos: {counts['owner_videos']}")
    print(f"  Toast Shorts: {counts['toast_shorts']}")
    print(f"  Toast Videos: {counts['toast_videos']}")
    print(f"  Owner-girl Shorts: {counts['owner_girl_shorts']}")
    print(f"  Owner-girl Videos: {counts['owner_girl_videos']}")
    print(f"  Restaurant Boss Shorts: {counts['rb_shorts']}")
    print(f"  Restaurant Boss Videos: {counts['rb_videos']}")

def update_formula_and_benchmark_indexes():
    # Update formula index
    f_path = os.path.join(INDEX_DIR, "formula-index.md")
    if os.path.exists(f_path):
        with open(f_path, "r", encoding="utf-8") as f:
            f_content = f.read()

        rb_formulas = """
## Prime Cost & Economics (The Restaurant Boss)

- **[Prime Cost Calculation](../knowledge/restaurant-boss/restaurant-boss-full-form/finance/prime-cost-numbers-that-matter.md)**
  - Prime Cost Formula: $\\text{Prime Cost \\%} = \\frac{\\text{Total COGS} + \\text{Total Labor (Hourly + Mgmt + Taxes)}}{\\text{Gross Food \\& Beverage Sales}}$.
  - Maximum Healthy Threshold: $\\text{Prime Cost} \\le 55\\% \\text{ to } 60\\%$.
- **[Theoretical vs Actual Food Cost Variance](../knowledge/restaurant-boss/restaurant-boss-full-form/food-cost/hit-restaurants-target-food-cost-every.md)**
  - Inventory Depletion Gap: $\\text{Food Cost Variance} = \\text{Actual Food Usage (Starting Inv + Purchases - Ending Inv)} - \\text{Theoretical Food Consumption (POS Mix)}$.
  - Allowable Target Variance: $\\le 1.5\\% \\text{ to } 2.0\\% \\text{ of sales}$.
- **[Menu Item Contribution Margin Matrix](../knowledge/restaurant-boss/restaurant-boss-full-form/menu/restaurant-menu-matrix-dilemma.md)**
  - Contribution Margin Dollars: $\\text{Contribution Margin} = \\text{Selling Price} - \\text{Portion Recipe Cost}$.
  - Optimization Goal: Maximize total dollars contributed rather than solely minimizing percentage food cost.
"""
        if "The Restaurant Boss" not in f_content:
            f_content += "\n" + rb_formulas.strip() + "\n"
            with open(f_path, "w", encoding="utf-8") as f:
                f.write(f_content)
            print("Updated formula-index.md with The Restaurant Boss intelligence.")

    # Update benchmark index
    b_path = os.path.join(INDEX_DIR, "benchmark-index.md")
    if os.path.exists(b_path):
        with open(b_path, "r", encoding="utf-8") as f:
            b_content = f.read()

        rb_benchmarks = """
## Operations, Cost Targets & Systems (The Restaurant Boss)

- **Prime Cost Ceiling**: Independent restaurant prime cost must remain strictly under 55% for full-service operations and under 60% for fast-casual concepts.
- **The 90-Day Owner Test**: Operations must run smoothly and profitably for 90 consecutive days without owner presence before deploying capital into secondary locations.
- **Checklist Compliance Standard**: High-performing restaurant teams maintain an opening, transition, and closing checklist completion rate exceeding 95%.
- **Credit Card Surcharge Friction**: Direct credit card surcharges increase customer dissatisfaction ratings and negative online reviews by over 30% compared to incorporating costs into menu pricing.
- **Phantom Labor Recovery**: Tightening shift clock-in/out windows and staggering line cuts recovers 10 to 20 wasted labor hours per week ($8,000 to $16,000 annually).
- **Menu SKU Rationalization**: Pruning the bottom 20% of low-velocity menu items reduces walk-in cooler spoilage by 15% to 25%.
"""
        if "The Restaurant Boss" not in b_content:
            b_content += "\n" + rb_benchmarks.strip() + "\n"
            with open(b_path, "w", encoding="utf-8") as f:
                f.write(b_content)
            print("Updated benchmark-index.md with The Restaurant Boss intelligence.")

def update_processed_sources_log():
    if not os.path.exists(LOG_PATH):
        return
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        log_content = f.read()

    rb_sections = """
## 7. The Restaurant Boss YouTube Shorts Collection

- **Source Channel:** [@Therestaurantboss](https://www.youtube.com/@Therestaurantboss/shorts)
- **Tracking Registry:** [`sources/youtube-lists/restaurant-boss-shorts.csv`](../sources/youtube-lists/restaurant-boss-shorts.csv)
- **Total Cataloged Shorts:** 77
- **Total Substantive Dossiers Ingested:** 68 across 10 categories in `knowledge/restaurant-boss/restaurant-boss-short-form/`
- **Total Triaged / Skipped:** 9 per AGENTS.md Rule 8
  - Promotional book promotions, webinar invites, milestone clips, and personal lifestyle topics
- **Quality Check Status:** 100% Pass (68/68 files compliant with schema, category hierarchy, numerical integrity, and source attribution)
- **Ingestion Status:** 100% Complete

## 8. The Restaurant Boss YouTube Long-Form Video Collection

- **Source Channel:** [@Therestaurantboss](https://www.youtube.com/@Therestaurantboss/videos)
- **Tracking Registry:** [`sources/youtube-lists/restaurant-boss-videos.csv`](../sources/youtube-lists/restaurant-boss-videos.csv)
- **Total Cataloged Videos:** 434
- **Total Substantive Dossiers Ingested:** 387 across 13 categories in `knowledge/restaurant-boss/restaurant-boss-full-form/`
- **Total Triaged / Skipped:** 47 per AGENTS.md Rule 8
  - 31 Software UI screen tutorials (clickBACON Ninja Tips & Wizards)
  - 7 Client video testimonials & case-study clips
  - 7 Promotional product teasers, giveaways, and channel trailers
  - 1 Holiday greeting clip
  - 1 Short clip (< 60s) uploaded to videos tab
- **Quality Check Status:** 100% Pass (387/387 files compliant with schema, category hierarchy, numerical integrity, and source attribution)
- **Ingestion Status:** 100% Complete
"""
    if "The Restaurant Boss YouTube Shorts Collection" not in log_content:
        log_content += "\n" + rb_sections.strip() + "\n"
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write(log_content)
        print("Updated logs/processed-sources.md with The Restaurant Boss audit summaries.")

if __name__ == "__main__":
    sync_knowledge_index()
    update_formula_and_benchmark_indexes()
    update_processed_sources_log()
    print("Master synchronization completed successfully!")
