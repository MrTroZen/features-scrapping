#!/usr/bin/env python3
"""
verify_toast_videos_quality.py

Comprehensive quality verification script for Toast long-form knowledge entries:
1. Category placement check (valid taxonomy folder).
2. File naming convention (lowercase kebab-case, .md).
3. Section architecture:
   - # Header
   - ## Overview
   - ## 1. <Section>
   - ## Numerical Benchmarks & Impact Metrics
   - ## Operational Implementation Takeaways
   - # Source (Channel, Video, URL)
4. Numerical presence: Ensures numerical benchmarks exist.
5. Tone check: Ensures no prohibited generic marketing hype.
"""

import os
import re
import sys

BASE_DIR = os.path.join("knowledge", "toast", "toast-full-form")
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

    lines = [line.strip() for line in content.splitlines()]

    # Header check
    if not lines or not lines[0].startswith("# "):
        errors.append("Missing top-level H1 title (# )")

    # Overview check
    if "## Overview" not in content:
        errors.append("Missing '## Overview' section")

    # Numbered section check
    if not re.search(r'## 1\.\s+', content):
        errors.append("Missing numbered section '## 1. '")

    # Numerical Benchmarks check
    if "## Numerical Benchmarks & Impact Metrics" not in content:
        errors.append("Missing '## Numerical Benchmarks & Impact Metrics' section")
    else:
        # Check if numbers exist in benchmarks
        bm_idx = content.find("## Numerical Benchmarks & Impact Metrics")
        src_idx = content.find("# Source")
        bm_section = content[bm_idx:src_idx if src_idx != -1 else len(content)]
        if not re.search(r'\d+', bm_section):
            errors.append("No numbers/percentages found in Numerical Benchmarks section")

    # Takeaways check
    if "## Operational Implementation Takeaways" not in content:
        errors.append("Missing '## Operational Implementation Takeaways' section")

    # Source block check
    if "# Source" not in content:
        errors.append("Missing terminal '# Source' block")
    else:
        if "- Channel: Toast, Inc." not in content:
            errors.append("Missing '- Channel: Toast, Inc.' in # Source block")
        if "- Video:" not in content:
            errors.append("Missing '- Video:' in # Source block")
        if not re.search(r'- URL:\s+https?://(www\.)?youtube\.com/watch\?v=[\w-]+', content):
            errors.append("Missing valid YouTube URL in # Source block")

    # Prohibited phrases
    lower_content = content.lower()
    for phrase in PROHIBITED_PHRASES:
        if phrase in lower_content:
            errors.append(f"Prohibited promotional phrase found: '{phrase}'")

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
