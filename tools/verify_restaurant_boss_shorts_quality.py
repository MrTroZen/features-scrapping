#!/usr/bin/env python3
"""
verify_restaurant_boss_shorts_quality.py

Quality verification script for Restaurant Boss short-form knowledge entries:
1. Category placement check (valid taxonomy folder).
2. File naming convention (lowercase kebab-case, .md).
3. Section architecture:
   - YAML frontmatter: serial, title, source, category, tags
   - # Key Information
   - # Numbers / Calculations
   - # Useful Method / Takeaway
   - # Context
   - # Source
4. Numerical presence: Ensures numerical benchmarks exist in Numbers / Calculations.
5. Tone check: Ensures no prohibited generic marketing hype.
"""

import os
import re
import sys

BASE_DIR = os.path.join("knowledge", "restaurant-boss", "restaurant-boss-short-form")
ALLOWED_CATEGORIES = {
    "finance", "food-cost", "labour", "inventory", "menu",
    "operations", "kitchen", "purchasing", "customers",
    "delivery", "payments", "forecasting", "marketing",
    "promotions", "social", "other"
}

PROHIBITED_PHRASES = [
    "game changer", "revolutionary", "all-in-one superpower",
    "magic bullet", "unbelievable results"
]

def verify_file(filepath):
    rel_path = os.path.relpath(filepath, BASE_DIR)
    parts = rel_path.split(os.sep)
    
    errors = []
    
    # 1. Directory category check
    if len(parts) != 2:
        errors.append(f"Incorrect directory depth: {rel_path}")
        return errors
        
    category, filename = parts
    if category not in ALLOWED_CATEGORIES:
        errors.append(f"Invalid taxonomy category: '{category}'")

    # 2. Filename check
    if not filename.endswith(".md"):
        errors.append("File must have .md extension")
    slug = filename[:-3]
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', slug):
        errors.append(f"Filename '{filename}' is not valid lowercase kebab-case")

    # 3. Content inspection
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Frontmatter check
    if not content.startswith("---\n"):
        errors.append("Missing YAML frontmatter opening (---)")
    else:
        fm_end = content.find("\n---\n", 4)
        if fm_end == -1:
            errors.append("Missing YAML frontmatter closing (---)")
        else:
            fm = content[4:fm_end]
            if "serial:" not in fm:
                errors.append("Missing 'serial:' in frontmatter")
            if "title:" not in fm:
                errors.append("Missing 'title:' in frontmatter")
            if "category:" not in fm:
                errors.append("Missing 'category:' in frontmatter")
            if "tags:" not in fm:
                errors.append("Missing 'tags:' in frontmatter")

    # Required sections check
    required_sections = [
        "# Key Information",
        "# Numbers / Calculations",
        "# Useful Method / Takeaway",
        "# Context",
        "# Source"
    ]
    for sec in required_sections:
        if sec not in content:
            errors.append(f"Missing required section '{sec}'")

    # Numbers in Numbers / Calculations
    if "# Numbers / Calculations" in content:
        num_idx = content.find("# Numbers / Calculations")
        take_idx = content.find("# Useful Method / Takeaway")
        num_section = content[num_idx:take_idx if take_idx != -1 else len(content)]
        if not re.search(r'\d+', num_section):
            errors.append("No numbers/percentages found in '# Numbers / Calculations' section")

    # Source check
    if "# Source" in content:
        src_idx = content.find("# Source")
        src_section = content[src_idx:]
        if not re.search(r'https?://(www\.)?youtube\.com/watch\?v=[\w-]+', src_section):
            errors.append("Missing valid YouTube video URL in '# Source' section")

    # Prohibited phrases in body analysis
    body_content = content[content.find("# Key Information"):] if "# Key Information" in content else content
    clean_body = re.sub(r"'[^']*'", "", body_content).lower()
    for phrase in PROHIBITED_PHRASES:
        if phrase in clean_body:
            errors.append(f"Prohibited promotional phrase found in analysis: '{phrase}'")

    return errors

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Error: Base directory '{BASE_DIR}' does not exist.")
        sys.exit(1)

    all_files = []
    for root, _, files in os.walk(BASE_DIR):
        for f in files:
            if f.endswith(".md"):
                all_files.append(os.path.join(root, f))

    print(f"Total files discovered in {BASE_DIR}: {len(all_files)}")
    
    total_errors = 0
    passed_files = 0

    for filepath in sorted(all_files):
        errs = verify_file(filepath)
        if errs:
            total_errors += len(errs)
            rel = os.path.relpath(filepath, BASE_DIR)
            print(f"[FAIL] {rel}:")
            for e in errs:
                print(f"   - {e}")
        else:
            passed_files += 1

    print("\n" + "=" * 50)
    print(f"Quality Check Results:")
    print(f"  Passed: {passed_files}/{len(all_files)} ({passed_files/len(all_files)*100:.1f}%)")
    print(f"  Total Errors: {total_errors}")
    print("=" * 50)

    if total_errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
