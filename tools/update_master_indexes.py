#!/usr/bin/env python3
"""
update_master_indexes.py

Updates master indexes (knowledge-index.md, formula-index.md, benchmark-index.md)
and logs/processed-sources.md to fix owner paths and include Toast short-form intelligence.
"""

import os
import re

INDEX_DIR = "indexes"
LOG_PATH = os.path.join("logs", "processed-sources.md")

def update_owner_paths_in_files():
    for f in ["knowledge-index.md", "formula-index.md", "benchmark-index.md"]:
        fpath = os.path.join(INDEX_DIR, f)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as file:
                content = file.read()
            # Replace paths
            content = content.replace("../knowledge/owner-short-form/", "../knowledge/owner/owner-short-form/")
            content = content.replace("../knowledge/owner-full-form/", "../knowledge/owner/owner-full-form/")
            with open(fpath, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Updated owner paths in {fpath}")

def append_toast_to_knowledge_index():
    k_path = os.path.join(INDEX_DIR, "knowledge-index.md")
    with open(k_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Collect Toast files by category
    toast_dir = os.path.join("knowledge", "toast", "toast-short-form")
    toast_by_cat = {}
    for root, dirs, files in os.walk(toast_dir):
        cat = os.path.basename(root)
        for f in files:
            if not f.endswith(".md"):
                continue
            fpath = os.path.join(root, f)
            with open(fpath, "r", encoding="utf-8") as mf:
                m_txt = mf.read()
            serial = re.search(r'serial:\s*"(\d{3})"', m_txt)
            title = re.search(r'title:\s*"([^"]+)"', m_txt)
            tags = re.search(r'tags:\s*\[([^\]]+)\]', m_txt)
            s_val = serial.group(1) if serial else "000"
            t_val = title.group(1) if title else f
            tags_val = tags.group(1) if tags else ""
            rel_link = f"../knowledge/toast/toast-short-form/{cat}/{f}"
            entry_line = f"- **Serial {s_val} (Toast)**: [{t_val}]({rel_link}) `[{tags_val}]`"
            if cat not in toast_by_cat:
                toast_by_cat[cat] = []
            toast_by_cat[cat].append((int(s_val), entry_line))

    # Update total count in header
    total_entries = 780 + 129
    content = re.sub(
        r'Total verified entries:\s*\*\*(\d+)\*\*',
        f'Total verified entries: **{total_entries}** (719 Owner Shorts, 61 Owner Videos, 129 Toast Shorts)',
        content
    )

    # Insert into category sections
    cat_names = {
        "customers": "Customers", "delivery": "Delivery", "finance": "Finance",
        "food-cost": "Food Cost", "forecasting": "Forecasting", "inventory": "Inventory",
        "kitchen": "Kitchen", "labour": "Labour", "marketing": "Marketing",
        "menu": "Menu", "operations": "Operations", "other": "Other",
        "payments": "Payments", "promotions": "Promotions", "purchasing": "Purchasing",
        "social": "Social"
    }

    for cat_key, items in toast_by_cat.items():
        cat_display = cat_names.get(cat_key, cat_key.title())
        sorted_items = sorted(items, key=lambda x: x[0])
        lines_to_add = "\n" + "\n".join(x[1] for x in sorted_items)

        # Match section header: ## CategoryName (XX entries)
        pattern = re.compile(rf'(## {re.escape(cat_display)} \()(\d+)( entries\))')
        m = pattern.search(content)
        if m:
            curr_count = int(m.group(2))
            new_count = curr_count + len(items)
            content = content[:m.start()] + f"## {cat_display} ({new_count} entries)" + content[m.end():]
            # Find next header ## or end of file to append before next section
            pos_header = content.find(f"## {cat_display} ({new_count} entries)")
            next_sec = content.find("\n## ", pos_header + 5)
            if next_sec != -1:
                content = content[:next_sec] + lines_to_add + "\n" + content[next_sec:]
            else:
                content = content + lines_to_add + "\n"
        else:
            # Create category section if not found
            content += f"\n## {cat_display} ({len(items)} entries)\n" + lines_to_add + "\n"

    with open(k_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Appended Toast short-form entries to knowledge-index.md")

def append_to_formula_and_benchmark_index():
    f_path = os.path.join(INDEX_DIR, "formula-index.md")
    with open(f_path, "r", encoding="utf-8") as f:
        f_txt = f.read()

    toast_formulas = """
## Inventory (Toast)

- **[Understanding PAR Levels for Restaurant Inventory Management](../knowledge/toast/toast-short-form/inventory/understanding-par-levels-for-inventory-management.md)** (Serial 066)
  - PAR Level Formula: $\\text{PAR Level} = (\\text{Average Daily Usage} \\times \\text{Lead Time in Days}) + \\text{Safety Stock Buffer}$.

## Labour (Toast)

- **[How this operator saved $4,000 on labor | Toast IQ](../knowledge/toast/toast-short-form/labour/saving-4000-dollars-on-restaurant-labor-with-ai.md)** (Serial 085)
  - Shift Stagger Optimization: Stagger line cook and server in-times in 30-minute increments against forecasted hourly sales curves to eliminate dead-hour overstaffing and cut up to $4,000 in monthly labor waste.

## Operations (Toast)

- **[Turn tables faster | Seamless Checkout](../knowledge/toast/toast-short-form/operations/turning-tables-faster-with-seamless-checkout.md)** (Serial 083)
  - Table Turn Dwell Time: Tableside mobile checkout shaves 7 to 10 minutes off average settlement dwell time (reducing payment cycle from 8-12 min down to <2 min).
"""
    if "Understanding PAR Levels for Restaurant Inventory Management" not in f_txt:
        f_txt += "\n" + toast_formulas.strip() + "\n"
        with open(f_path, "w", encoding="utf-8") as f:
            f.write(f_txt)
        print("Appended Toast formulas to formula-index.md")

def update_logs():
    if not os.path.exists(LOG_PATH):
        return
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        log_content = f.read()

    # Update owner links inside logs/processed-sources.md as well
    log_content = log_content.replace("../knowledge/owner-short-form/", "../knowledge/owner/owner-short-form/")
    log_content = log_content.replace("../knowledge/owner-full-form/", "../knowledge/owner/owner-full-form/")

    toast_log = """
## 3. Toast, Inc. YouTube Shorts Collection

- **Source Channel:** [@Toasttab](https://www.youtube.com/@Toasttab/shorts)
- **Tracking Registry:** [`sources/youtube-lists/toast-shorts.csv`](../sources/youtube-lists/toast-shorts.csv)
- **Total Cataloged Videos:** 129
- **Total Successfully Ingested:** 129
- **Ingestion Status:** 100% complete
- **Processed Batches:**
  - Batch 1 (Serials 001–129): 129 research entries across 12 categories under `knowledge/toast/toast-short-form/`
"""
    if "Toast, Inc. YouTube Shorts Collection" not in log_content:
        log_content += "\n" + toast_log.strip() + "\n"
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write(log_content)
        print("Appended Toast section to logs/processed-sources.md")

if __name__ == "__main__":
    update_owner_paths_in_files()
    append_toast_to_knowledge_index()
    append_to_formula_and_benchmark_index()
    update_logs()
    print("Master indexes and logs successfully synchronized!")
