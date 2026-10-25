#!/usr/bin/env python3
"""
verify_matt_plapp_videos_quality.py

Verifies 100% compliance of knowledge/matt-plapp/matt-plapp-full-form/ dossiers:
- Proper lowercase kebab-case naming
- Valid taxonomy category folder
- Complete headings and structure
- Verified numerical benchmarks
- Source attribution with valid YouTube URL
"""

import glob
import os
import re
import sys

BASE_DIR = os.path.join("knowledge", "matt-plapp", "matt-plapp-full-form")

VALID_CATEGORIES = {
    "accounting", "analytics", "bar-beverage", "compliance", "cost-control",
    "customers", "delivery", "finance", "kitchen", "labour", "marketing",
    "menu", "operations", "ordering", "promotions", "technology"
}

REQUIRED_SECTIONS = [
    "## Overview",
    "## 1. ",
    "## 2. ",
    "## Numerical Benchmarks & Impact Metrics",
    "## Operational Implementation Takeaways",
    "# Source"
]

def verify_videos():
    files = glob.glob(os.path.join(BASE_DIR, "**", "*.md"), recursive=True)
    print(f"Total Matt Plapp video dossiers found: {len(files)}")
    assert len(files) == 846, f"Expected exactly 846 files, got {len(files)}"

    errors = []

    for filepath in files:
        rel_path = os.path.relpath(filepath, BASE_DIR)
        parts = rel_path.split(os.sep)
        if len(parts) != 2:
            errors.append(f"Invalid directory nesting: {rel_path}")
            continue

        cat_dir, filename = parts[0], parts[1]

        # Category check
        if cat_dir not in VALID_CATEGORIES:
            errors.append(f"Invalid category folder '{cat_dir}' in {rel_path}")

        # Filename check (lowercase kebab-case)
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*\.md$', filename):
            errors.append(f"Filename not lowercase kebab-case: {filename}")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Title check
        if not content.startswith("# Restaurant Marketing Intelligence:"):
            errors.append(f"Missing main H1 title in {rel_path}")

        # Section check
        for sec in REQUIRED_SECTIONS:
            if sec not in content:
                errors.append(f"Missing required section '{sec}' in {rel_path}")

        # Numbers check
        nums_match = re.search(r'## Numerical Benchmarks & Impact Metrics\s*\n(.*?)(?=\n---|\n#|$)', content, re.DOTALL)
        if not nums_match or not re.search(r'(\d+%|\$\d+|\d+)', nums_match.group(1)):
            errors.append(f"Missing numerical benchmarks in {rel_path}")

        # Source URL check
        if "https://www.youtube.com/" not in content:
            errors.append(f"Missing or invalid YouTube source URL in {rel_path}")

    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for e in errors[:20]:
            print(f"  - {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {len(files)} Matt Plapp long-form video dossiers passed 100% quality checks!")

if __name__ == "__main__":
    verify_videos()
