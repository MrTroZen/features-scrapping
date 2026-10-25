#!/usr/bin/env python3
"""
verify_wilson_fb_videos_quality.py

Comprehensive quality verification script for Wilson F&B long-form knowledge entries:
1. Category placement check (valid taxonomy folder).
2. File naming convention (lowercase kebab-case, .md).
3. Section architecture:
   - # Header
   - ## Overview
   - ## 1. <Section 1>
   - ## 2. <Section 2>
   - ## Numerical Benchmarks & Impact Metrics
   - ## Operational Implementation Takeaways
   - # Source (Channel, Video, URL)
4. Numerical presence: Ensures numerical benchmarks exist.
5. Tone check: Ensures no prohibited generic marketing hype.
"""

import os
import re
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.join("knowledge", "wilson-fb", "wilson-fb-full-form")
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
    if not re.search(r'## 2\.\s+', content):
        errors.append("Missing numbered section '## 2. '")

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
        if "- Channel: Wilson F&B" not in content:
            errors.append("Missing '- Channel: Wilson F&B' in # Source block")
        if "- Video:" not in content:
            errors.append("Missing '- Video:' in # Source block")
        if not re.search(r'- URL:\s+https?://(www\.)?youtube\.com/watch\?v=[\w-]+', content):
            errors.append("Missing valid YouTube URL in # Source block")

    # Tone check (ignore quoted titles)
    content_no_quotes = re.sub(r"'[^']*'", "", content)
    content_lower = content_no_quotes.lower()
    for phrase in PROHIBITED_PHRASES:
        if phrase in content_lower:
            errors.append(f"Prohibited promotional phrase found: '{phrase}'")

    return errors

def main():
    print("=" * 60)
    print("Running Quality Verification on Wilson F&B Long-Form Dossiers")
    print("=" * 60)

    total_files = 0
    passed_files = 0
    failed_files = 0
    failures = {}

    for root, dirs, files in os.walk(BASE_DIR):
        for f in sorted(files):
            if f.endswith(".md") and not f.startswith("."):
                total_files += 1
                filepath = os.path.join(root, f)
                errs = verify_file(filepath)
                if errs:
                    failed_files += 1
                    failures[filepath] = errs
                else:
                    passed_files += 1

    print(f"\nFiles Inspected: {total_files}")
    print(f"Passed:          {passed_files}")
    print(f"Failed:          {failed_files}")

    if failures:
        print("\nFAILURE DETAILS:")
        for path, errs in failures.items():
            rel = os.path.relpath(path, BASE_DIR)
            print(f"\n  [FAIL] {rel}:")
            for e in errs:
                print(f"    - {e}")
        sys.exit(1)
    else:
        print("\nSUCCESS: 100.0% of Wilson F&B long-form dossiers pass all quality standards!")
        print("=" * 60)

if __name__ == "__main__":
    main()
