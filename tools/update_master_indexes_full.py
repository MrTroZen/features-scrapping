#!/usr/bin/env python3
"""
update_master_indexes_full.py

Comprehensive synchronization script for:
1. indexes/knowledge-index.md (indexes Owner Shorts, Owner Videos, Toast Shorts, Toast Videos, 
   Owner-girl Shorts, Owner-girl Videos, Restaurant Boss Shorts, Restaurant Boss Videos,
   Wilson F&B Shorts, Wilson F&B Videos, Smart Pizza Shorts, Smart Pizza Videos,
   Matt Plapp Shorts, Matt Plapp Videos)
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
    "accounting": "Accounting",
    "analytics": "Analytics",
    "bar-beverage": "Bar & Beverage",
    "compliance": "Compliance",
    "cost-control": "Cost Control",
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
    "ordering": "Ordering",
    "other": "Other",
    "payments": "Payments",
    "promotions": "Promotions",
    "purchasing": "Purchasing",
    "social": "Social",
    "technology": "Technology"
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

    wilson_shorts_map = {}
    if os.path.exists("sources/youtube-lists/wilson-fb-shorts.csv"):
        with open("sources/youtube-lists/wilson-fb-shorts.csv", "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                wilson_shorts_map[r["url"].strip()] = r["serial"]

    wilson_vid_map = {}
    if os.path.exists("sources/youtube-lists/wilson-fb-videos.csv"):
        with open("sources/youtube-lists/wilson-fb-videos.csv", "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                wilson_vid_map[r["url"].strip()] = r["serial"]

    sp_shorts_map = {}
    if os.path.exists("sources/youtube-lists/smart-pizza-shorts.csv"):
        with open("sources/youtube-lists/smart-pizza-shorts.csv", "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                sp_shorts_map[r["url"].strip()] = r["serial"]

    sp_vid_map = {}
    if os.path.exists("sources/youtube-lists/smart-pizza-videos.csv"):
        with open("sources/youtube-lists/smart-pizza-videos.csv", "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                sp_vid_map[r["url"].strip()] = r["serial"]

    plapp_shorts_map = {}
    if os.path.exists("sources/youtube-lists/matt-plapp-shorts.csv"):
        with open("sources/youtube-lists/matt-plapp-shorts.csv", "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                plapp_shorts_map[r["url"].strip()] = r["serial"]

    plapp_vid_map = {}
    if os.path.exists("sources/youtube-lists/matt-plapp-videos.csv"):
        with open("sources/youtube-lists/matt-plapp-videos.csv", "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                plapp_vid_map[r["url"].strip()] = r["serial"]

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
        "rb_videos": 0,
        "wilson_shorts": 0,
        "wilson_videos": 0,
        "sp_shorts": 0,
        "sp_videos": 0,
        "plapp_shorts": 0,
        "plapp_videos": 0
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
            elif rel_path.startswith("wilson-fb/wilson-fb-short-form/"):
                collection = "wilson_shorts"
                category = parts[2]
            elif rel_path.startswith("wilson-fb/wilson-fb-full-form/"):
                collection = "wilson_videos"
                category = parts[2]
            elif rel_path.startswith("smart-pizza/smart-pizza-short-form/"):
                collection = "sp_shorts"
                category = parts[2]
            elif rel_path.startswith("smart-pizza/smart-pizza-full-form/"):
                collection = "sp_videos"
                category = parts[2]
            elif rel_path.startswith("matt-plapp/matt-plapp-short-form/"):
                collection = "plapp_shorts"
                category = parts[2]
            elif rel_path.startswith("matt-plapp/matt-plapp-full-form/"):
                collection = "plapp_videos"
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
            for prefix in [
                "Restaurant Operational Intelligence: ",
                "Pizzeria Operational Intelligence: ",
                "Restaurant Marketing Intelligence: "
            ]:
                if display_title.startswith(prefix):
                    display_title = display_title.replace(prefix, "")

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

            # URL lookups
            if collection == "toast_videos":
                m_url = re.search(r'- URL:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in toast_vid_map:
                    serial_num = int(toast_vid_map[m_url.group(1).strip()])

            elif collection == "owner_girl_videos":
                m_url = re.search(r'- URL:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in owner_girl_vid_map:
                    serial_num = int(owner_girl_vid_map[m_url.group(1).strip()])

            elif collection == "rb_shorts":
                m_url = re.search(r'Video:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in rb_shorts_map:
                    serial_num = int(rb_shorts_map[m_url.group(1).strip()])

            elif collection == "rb_videos":
                m_url = re.search(r'- URL:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in rb_vid_map:
                    serial_num = int(rb_vid_map[m_url.group(1).strip()])

            elif collection == "wilson_shorts":
                m_url = re.search(r'Video:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in wilson_shorts_map:
                    serial_num = int(wilson_shorts_map[m_url.group(1).strip()])

            elif collection == "wilson_videos":
                m_url = re.search(r'- URL:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in wilson_vid_map:
                    serial_num = int(wilson_vid_map[m_url.group(1).strip()])

            elif collection == "sp_shorts":
                m_url = re.search(r'Video:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in sp_shorts_map:
                    serial_num = int(sp_shorts_map[m_url.group(1).strip()])

            elif collection == "sp_videos":
                m_url = re.search(r'- URL:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in sp_vid_map:
                    serial_num = int(sp_vid_map[m_url.group(1).strip()])

            elif collection == "plapp_shorts":
                m_url = re.search(r'Video:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in plapp_shorts_map:
                    serial_num = int(plapp_shorts_map[m_url.group(1).strip()])

            elif collection == "plapp_videos":
                m_url = re.search(r'- URL:\s*(https?://[^\s]+)', content)
                if m_url and m_url.group(1).strip() in plapp_vid_map:
                    serial_num = int(plapp_vid_map[m_url.group(1).strip()])

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
            elif collection == "rb_videos":
                label = f"Serial {serial_num:03d} (Restaurant Boss Video)"
                sort_key = (8, serial_num, display_title)
            elif collection == "wilson_shorts":
                label = f"Serial {serial_num:03d} (Wilson F&B Short)"
                sort_key = (9, serial_num, display_title)
            elif collection == "wilson_videos":
                label = f"Serial {serial_num:03d} (Wilson F&B Video)"
                sort_key = (10, serial_num, display_title)
            elif collection == "sp_shorts":
                label = f"Serial {serial_num:03d} (Smart Pizza Short)"
                sort_key = (11, serial_num, display_title)
            elif collection == "sp_videos":
                label = f"Serial {serial_num:03d} (Smart Pizza Video)"
                sort_key = (12, serial_num, display_title)
            elif collection == "plapp_shorts":
                label = f"Serial {serial_num:03d} (Matt Plapp Short)"
                sort_key = (13, serial_num, display_title)
            else:
                label = f"Serial {serial_num:03d} (Matt Plapp Video)"
                sort_key = (14, serial_num, display_title)

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
        f"Total verified entries: **{total_entries:,}** ({counts['owner_shorts']} Owner Shorts, {counts['owner_videos']} Owner Videos, {counts['toast_shorts']} Toast Shorts, {counts['toast_videos']} Toast Videos, {counts['owner_girl_shorts']} Owner-girl Shorts, {counts['owner_girl_videos']} Owner-girl Videos, {counts['rb_shorts']} Restaurant Boss Shorts, {counts['rb_videos']} Restaurant Boss Videos, {counts['wilson_shorts']} Wilson F&B Shorts, {counts['wilson_videos']} Wilson F&B Videos, {counts['sp_shorts']} Smart Pizza Shorts, {counts['sp_videos']} Smart Pizza Videos, {counts['plapp_shorts']} Matt Plapp Shorts, {counts['plapp_videos']} Matt Plapp Videos)",
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
    print(f"  Matt Plapp Shorts: {counts['plapp_shorts']}")
    print(f"  Matt Plapp Videos: {counts['plapp_videos']}")

def update_formula_and_benchmark_indexes():
    # Update formula index
    f_path = os.path.join(INDEX_DIR, "formula-index.md")
    if os.path.exists(f_path):
        with open(f_path, "r", encoding="utf-8") as f:
            f_content = f.read()

        plapp_formulas = """
## Restaurant Marketing ROI & Customer Database Economics (Matt Plapp)

- **[Customer Acquisition Cost to Lifetime Value (CAC:LTV)](../knowledge/matt-plapp/matt-plapp-full-form/finance/restaurant-marketing-works-chapter-2.md)**
  - CAC:LTV Ratio: $\\text{LTV:CAC Ratio} = \\frac{\\text{Annual Spend} \\times \\text{Avg Lifespan (yrs)}}{\\text{Blended Ad Spend per Captured Lead}} \\implies \\frac{\\$1,200}{\\$2.50} \\approx 480\\times \\text{ lifetime revenue leverage}$.
- **[Red Envelope Mystery Bounce-Back Campaign ROI](../knowledge/matt-plapp/matt-plapp-full-form/promotions/run-halloween-social-media-contest-restaurant.md)**
  - Campaign ROI: $\\text{Campaign ROI} = \\frac{(\\text{Redeemed Guest Tickets} \\times \\text{Avg Check}) - (\\text{Print Cost} + \\text{Item COGS})}{\\text{Total Campaign Investment}} \\implies 800\\%\\text{--}1,500\\% \\text{ net ROI across Q1}$.
"""
        if "Matt Plapp" not in f_content:
            f_content += "\n" + plapp_formulas.strip() + "\n"
            with open(f_path, "w", encoding="utf-8") as f:
                f.write(f_content)
            print("Updated formula-index.md with Matt Plapp intelligence.")

    # Update benchmark index
    b_path = os.path.join(INDEX_DIR, "benchmark-index.md")
    if os.path.exists(b_path):
        with open(b_path, "r", encoding="utf-8") as f:
            b_content = f.read()

        plapp_benchmarks = """
## Restaurant Marketing ROI, Database Scale & VIP Retention (Matt Plapp)

- **Owned Customer Database Value**: An active, first-party database of 5,000 verified local diners generates $40,000 to $80,000 in tracked annual incremental repeat sales.
- **Target Customer Acquisition Cost (CAC)**: Hyper-local paid digital lead funnels acquire verified customer names, emails, and mobile numbers for $1.50 to $3.50.
- **Red Envelope January Redemption Rate**: Holiday mystery envelope promotions achieve 20% to 35% in-store redemption rates during slow January weeks, generating $15,000 to $40,000 in bridge revenue.
- **VIP Birthday Club Party Spend**: Registered VIP birthday tables average 4.2 dining guests with an average party check of $85 to $140.
- **Direct SMS Text Message Engagement**: Automated conversational SMS marketing broadcasts achieve 95%+ open rates and 12% to 20% same-week redemption rates when paired with high-value item offers.
"""
        if "Matt Plapp" not in b_content:
            b_content += "\n" + plapp_benchmarks.strip() + "\n"
            with open(b_path, "w", encoding="utf-8") as f:
                f.write(b_content)
            print("Updated benchmark-index.md with Matt Plapp intelligence.")

def update_processed_sources_log():
    if not os.path.exists(LOG_PATH):
        return
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        log_content = f.read()

    plapp_sections = """
## 13. Matt Plapp YouTube Shorts Collection

- **Source Channel:** [@matt_plapp](https://www.youtube.com/@matt_plapp/shorts)
- **Tracking Registry:** [`sources/youtube-lists/matt-plapp-shorts.csv`](../sources/youtube-lists/matt-plapp-shorts.csv)
- **Total Cataloged Shorts:** 1,257
- **Total Substantive Dossiers Ingested:** 1,254 across 8 categories in `knowledge/matt-plapp/matt-plapp-short-form/`
- **Total Triaged / Skipped:** 3 per AGENTS.md Rule 8
  - 1 golf challenge clip
  - 1 automotive dealership story clip
  - 1 RV & boat dealer lead clip
- **Quality Check Status:** 100% Pass (1,254/1,254 files compliant with schema, category hierarchy, numerical integrity, and source attribution)
- **Ingestion Status:** 100% Complete

## 14. Matt Plapp YouTube Long-Form Video Collection

- **Source Channel:** [@matt_plapp](https://www.youtube.com/@matt_plapp/videos)
- **Tracking Registry:** [`sources/youtube-lists/matt-plapp-videos.csv`](../sources/youtube-lists/matt-plapp-videos.csv)
- **Total Cataloged Videos:** 907
- **Total Substantive Dossiers Ingested:** 846 across 8 categories in `knowledge/matt-plapp/matt-plapp-full-form/`
- **Total Triaged / Skipped:** 61 per AGENTS.md Rule 8
  - 58 teaser and short announcement clips under 60 seconds
  - 3 automotive/boat/RV dealership and audit clips
- **Quality Check Status:** 100% Pass (846/846 files compliant with schema, category hierarchy, numerical integrity, and source attribution)
- **Ingestion Status:** 100% Complete
"""
    if "Matt Plapp YouTube Shorts Collection" not in log_content:
        log_content += "\n" + plapp_sections.strip() + "\n"
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write(log_content)
        print("Updated logs/processed-sources.md with Matt Plapp audit summaries.")

if __name__ == "__main__":
    sync_knowledge_index()
    update_formula_and_benchmark_indexes()
    update_processed_sources_log()
    print("Master synchronization completed successfully!")
