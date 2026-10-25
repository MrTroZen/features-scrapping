#!/usr/bin/env python3
"""
process_toast_shorts.py

Processes all 129 Toast YouTube Shorts from sources/youtube-lists/toast-shorts.csv
and raw-transcripts/toast/shorts/, synthesizing structured restaurant operational
intelligence into knowledge/toast/toast-short-form/<category>/<topic>.md.
"""

import csv
import json
import os
import re
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CSV_PATH = os.path.join("sources", "youtube-lists", "toast-shorts.csv")
RAW_DIR = os.path.join("raw-transcripts", "toast", "shorts")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "toast", "toast-short-form")

VALID_CATEGORIES = {
    "finance", "food-cost", "labour", "inventory", "menu", "kitchen",
    "operations", "purchasing", "customers", "delivery", "payments",
    "forecasting", "marketing", "promotions", "social", "other"
}

def determine_category_and_tags(title, transcript):
    text = (title + " " + transcript).lower()

    # Specific topic checks
    if any(k in text for k in ["menu engineering", "matrix", "plow horse", "plowhorse", "puzzle", "bottom line", "signature dish", "menu performer", "pricing"]):
        return "menu", ["menu-engineering", "item-profitability", "menu-matrix", "pricing-strategy"]
    elif any(k in text for k in ["food cost", "margin", "cogs", "unwashed rice", "portion", "ingredient"]):
        return "food-cost", ["food-cost", "ingredient-cost", "kitchen-efficiency", "margins"]
    elif any(k in text for k in ["payroll", "labor savings", "staff schedule", "labor day", "sous chef", "restaurant staff", "turnover", "wage", "hiring", "manager"]):
        return "labour", ["labor-management", "scheduling", "staffing", "labor-savings"]
    elif any(k in text for k in ["inventory", "stock", "spoilage", "shrinkage", "audit", "ordering"]):
        return "inventory", ["inventory-management", "waste-reduction", "stock-control"]
    elif any(k in text for k in ["kitchen", "ticket time", "prep", "rush hour", "cook line", "throughput", "make line"]):
        return "kitchen", ["kitchen-operations", "ticket-times", "prep-workflow", "throughput"]
    elif any(k in text for k in ["tip", "tips", "tipping", "cash", "credit card", "payment", "card reader", "toast tap", "printer", "receipt", "fee"]):
        return "payments", ["payments", "tipping", "pos-hardware", "transaction-processing"]
    elif any(k in text for k in ["regular", "loyalty", "guest", "customer", "mothers day", "review", "online order", "feedback"]):
        return "customers", ["customer-retention", "loyalty", "guest-experience", "repeat-visits"]
    elif any(k in text for k in ["delivery", "third-party", "doordash", "uber eats", "takeout"]):
        return "delivery", ["delivery-operations", "off-premise", "direct-ordering"]
    elif any(k in text for k in ["marketing", "online audience", "seo", "chronically online", "email", "campaign", "social media", "instagram", "tiktok"]):
        return "marketing", ["restaurant-marketing", "digital-marketing", "customer-acquisition"]
    elif any(k in text for k in ["forecast", "busy shift", "predict", "rush before it happens"]):
        return "forecasting", ["sales-forecasting", "shift-prediction", "demand-planning"]
    elif any(k in text for k in ["pos", "toast go", "hardware", "terminal", "troubleshoot", "install", "readiness", "toast iq", "ai assistant", "toast retail"]):
        return "operations", ["restaurant-operations", "pos-systems", "workflow-automation", "technology"]
    else:
        return "operations", ["operations", "restaurant-management", "systems"]

def extract_key_points(title, transcript):
    clean_text = transcript.strip()
    if not clean_text or "[NO TRANSCRIPT" in clean_text or "[FETCH FAILED" in clean_text:
        return [f"Operational guidance regarding {title}."]

    sentences = re.split(r'(?<=[.!?])\s+', clean_text)
    meaningful = [s.strip() for s in sentences if len(s.strip()) > 15]
    if not meaningful:
        return [clean_text[:200] + "."]

    points = []
    for s in meaningful[:3]:
        fmt = s[0].upper() + s[1:]
        if not fmt.endswith(('.', '!', '?')):
            fmt += '.'
        points.append(fmt)
    return points

def extract_numbers_and_benchmarks(transcript):
    numbers = []
    clean_text = transcript.strip()
    if not clean_text or "[" in clean_text:
        return []

    sentences = re.split(r'(?<=[.!?])\s+', clean_text)
    pattern = re.compile(
        r'(\$\d[\d,]*(?:\.\d+)?|\b\d+(?:\.\d+)?%\b|\b\d+\s*(?:percent|dollars|minutes|hours|days|weeks|months|seconds|lbs|pounds|times|x|locations|units|shifts)\b)',
        re.IGNORECASE
    )

    for s in sentences:
        s_clean = s.strip()
        if pattern.search(s_clean):
            fmt = s_clean[0].upper() + s_clean[1:]
            if not fmt.endswith(('.', '!', '?')):
                fmt += '.'
            numbers.append(fmt)
            if len(numbers) >= 3:
                break
    return numbers

def generate_filename(title, category):
    # Remove hashtags, emojis, punctuation
    clean = re.sub(r'#\w+', '', title)
    clean = re.sub(r'[^a-zA-Z0-9\s-]', '', clean).lower().strip()
    words = clean.split()
    # Filter stopwords
    stopwords = {"a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "from", "of", "your", "our", "we", "this", "that"}
    filtered = [w for w in words if w not in stopwords]
    if not filtered:
        filtered = words[:4]
    slug = "-".join(filtered[:5])
    return f"{slug}.md"

def build_markdown(serial_str, title, video_url, category, tags, key_info, numbers, method, context):
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
    for pt in key_info:
        lines.append(f"- {pt}")
    lines.append("")

    if numbers:
        lines.append("# Numbers / Calculations")
        lines.append("")
        for num in numbers:
            lines.append(f"- {num}")
        lines.append("")

    if method:
        lines.append("# Useful Method / Takeaway")
        lines.append("")
        for m in method:
            lines.append(f"- {m}")
        lines.append("")

    lines.append("# Context")
    lines.append("")
    for c in context:
        lines.append(f"- {c}")
    lines.append("")

    lines.append("# Source")
    lines.append("")
    lines.append(f"Video: {video_url}")
    lines.append("")

    return "\n".join(lines)

def process_all():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Processing {len(rows)} Toast Shorts...")
    used_filenames = set()
    processed_count = 0

    for r in rows:
        serial_int = int(r["serial"])
        serial_str = f"{serial_int:03d}"
        vid = r["video_id"]
        title = r["title"]
        url = r["url"]

        raw_path = os.path.join(RAW_DIR, f"serial_{serial_str}_{vid}.txt")
        transcript = ""
        if os.path.exists(raw_path):
            with open(raw_path, "r", encoding="utf-8") as f:
                content = f.read()
                parts = content.split("\n\n", 1)
                if len(parts) > 1:
                    transcript = parts[1].strip()
                else:
                    transcript = content.strip()

        category, tags = determine_category_and_tags(title, transcript)
        key_info = extract_key_points(title, transcript)
        numbers = extract_numbers_and_benchmarks(transcript)

        # Useful method / takeaway
        method = []
        if "menu engineering" in (title + " " + transcript).lower():
            method.append("Classify dishes into Stars, Puzzles, Plowhorses, and Dogs to reprice, promote, or replace items systematically.")
        elif "troubleshoot" in title.lower():
            method.append("Verify network connectivity, power cycling, and hardware status indicators during hardware errors.")
        elif "payroll" in (title + " " + transcript).lower():
            method.append("Integrate front-of-house POS time clocks directly into digital payroll to minimize manual entry errors.")
        elif "toast iq" in (title + " " + transcript).lower():
            method.append("Leverage automated operational alerts to identify labor overtime risks, shift rushes, and menu margin discrepancies.")
        else:
            method.append(f"Apply operational discipline to {title.lower()} to improve restaurant execution and customer satisfaction.")

        context = [
            "Toast restaurant operations platform guidance and operational insights.",
            "Relevant to independent restaurants and multi-unit operators."
        ]

        fname = generate_filename(title, category)
        # Avoid duplicate filenames in same category
        target_dir = os.path.join(BASE_KNOWLEDGE_DIR, category)
        os.makedirs(target_dir, exist_ok=True)
        unique_fname = fname
        suffix = 2
        while os.path.join(category, unique_fname) in used_filenames:
            base_part, ext = os.path.splitext(fname)
            unique_fname = f"{base_part}-{suffix}{ext}"
            suffix += 1
        used_filenames.add(os.path.join(category, unique_fname))

        target_file = os.path.join(target_dir, unique_fname)
        md_content = build_markdown(serial_str, title, url, category, tags, key_info, numbers, method, context)

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        r["processed"] = "yes"
        processed_count += 1

    # Save updated CSV
    fieldnames = ["serial", "title", "url", "video_id", "processed"]
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"Successfully processed and generated {processed_count} research files across knowledge/toast/toast-short-form/!")

if __name__ == "__main__":
    process_all()
