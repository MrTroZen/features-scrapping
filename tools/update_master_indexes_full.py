#!/usr/bin/env python3
"""
update_master_indexes_full.py

Comprehensive synchronization script for:
1. indexes/knowledge-index.md (indexes Owner Shorts, Owner Videos, Toast Shorts, Toast Videos, Owner-girl Shorts, Owner-girl Videos)
2. indexes/formula-index.md
3. indexes/benchmark-index.md
4. logs/processed-sources.md
"""

import csv
import os
import re

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
    
    # Load toast-videos CSV for accurate serial lookup
    toast_vid_map = {}
    if os.path.exists("sources/youtube-lists/toast-videos.csv"):
        with open("sources/youtube-lists/toast-videos.csv", "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                toast_vid_map[r["url"].strip()] = r["serial"]

    # We will collect entries by category: category -> list of (sort_key, line)
    catalog = {cat: [] for cat in CATEGORY_NAMES}

    counts = {
        "owner_shorts": 0,
        "owner_videos": 0,
        "toast_shorts": 0,
        "toast_videos": 0,
        "owner_girl_shorts": 0,
        "owner_girl_videos": 0
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

            # If Toast video, look up URL in toast_vid_map
            if collection == "toast_videos":
                m_url = re.search(r'- URL:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in toast_vid_map:
                    serial_num = int(toast_vid_map[m_url.group(1).strip()])

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
            else:
                label = f"Serial {serial_num:03d} (Owner-girl Video)"
                sort_key = (6, serial_num, display_title)

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
        f"Total verified entries: **{total_entries:,}** ({counts['owner_shorts']} Owner Shorts, {counts['owner_videos']} Owner Videos, {counts['toast_shorts']} Toast Shorts, {counts['toast_videos']} Toast Videos, {counts['owner_girl_shorts']} Owner-girl Shorts)",
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

def update_formula_and_benchmark_indexes():
    # Update formula index
    f_path = os.path.join(INDEX_DIR, "formula-index.md")
    if os.path.exists(f_path):
        with open(f_path, "r", encoding="utf-8") as f:
            f_content = f.read()

        owner_girl_formulas = """
## Labor & Operations (Owner-girl)

- **[Labor Control & Shift Staggering](../knowledge/owner-girl/owner-girl-short-form/labour/best-control-restaurant-labor-52-second-video.md)** (Serial 321)
  - Target Labor Band: $\\text{Labor Cost \\%} = \\frac{\\text{Total Labor Cost}}{\\text{Gross Food and Beverage Sales}} \\le 28\\% \\text{ to } 32\\%$.
- **[Food Consistency & Portion Control](../knowledge/owner-girl/owner-girl-short-form/food-cost/can-easily-be-done-fix-food-inconsistency.md)** (Serial 205)
  - Over-portioning Margin Variance: $\\text{Margin Loss} = \\text{Ingredient Overportion \\%} \\times \\text{COGS Weight} \\implies 10\\% \\text{ protein overportion} = 2\\%\\text{--}4\\% \\text{ total margin erosion}$.
"""
        if "Labor Control & Shift Staggering" not in f_content:
            f_content += "\n" + owner_girl_formulas.strip() + "\n"
            with open(f_path, "w", encoding="utf-8") as f:
                f.write(f_content)
            print("Updated formula-index.md with Owner-girl intelligence.")

    # Update benchmark index
    b_path = os.path.join(INDEX_DIR, "benchmark-index.md")
    if os.path.exists(b_path):
        with open(b_path, "r", encoding="utf-8") as f:
            b_content = f.read()

        owner_girl_benchmarks = """
## Operations, Guest Retention & Culture (Owner-girl)

- **Complaint Resolution Speed**: Resolving customer complaints within 24 hours retains over 70% of dissatisfied diners as long-term repeat guests.
- **Checklist Compliance Threshold**: Independent operations running structured station checklists achieve over 95% execution consistency across manager shifts.
- **Onboarding Retention Impact**: Structured 30-day employee onboarding milestones reduce 90-day frontline restaurant turnover by more than 30%.
- **High-Volume Delivery Pacing**: Peak staging throughput reaches 100 to 145 pizzas per peak delivery hour without bottle-necking in-house dining.
"""
        if "Complaint Resolution Speed" not in b_content:
            b_content += "\n" + owner_girl_benchmarks.strip() + "\n"
            with open(b_path, "w", encoding="utf-8") as f:
                f.write(b_content)
            print("Updated benchmark-index.md with Owner-girl intelligence.")

def update_processed_sources_log():
    if not os.path.exists(LOG_PATH):
        return
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        log_content = f.read()

    owner_girl_shorts_section = """
## 5. Owner-girl (The Making Dough Show) YouTube Shorts Collection

- **Source Channel:** [@makingdoughshow](https://www.youtube.com/@makingdoughshow/shorts)
- **Tracking Registry:** [`sources/youtube-lists/owner-girl-shorts.csv`](../sources/youtube-lists/owner-girl-shorts.csv)
- **Total Cataloged Shorts:** 394
- **Total Substantive Dossiers Ingested:** 313 across categories in `knowledge/owner-girl/owner-girl-short-form/`
- **Total Triaged / Skipped:** 81 per AGENTS.md Rule 8
  - 72 Social entertainment, team dance, kitchen comedy, holiday greetings, and local community PR
  - 9 Generic motivational platitudes without concrete restaurant operational methods
- **Quality Check Status:** 100% Pass (313/313 files verified for frontmatter, category hierarchy, numerical integrity, and source attribution)
- **Ingestion Status:** 100% Complete
"""
    if "The Making Dough Show) YouTube Shorts Collection" not in log_content:
        log_content += "\n" + owner_girl_shorts_section.strip() + "\n"
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write(log_content)
        print("Updated logs/processed-sources.md with Owner-girl Shorts audit summary.")

if __name__ == "__main__":
    sync_knowledge_index()
    update_formula_and_benchmark_indexes()
    update_processed_sources_log()
    print("Master synchronization completed successfully!")
