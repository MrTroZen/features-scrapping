#!/usr/bin/env python3
"""
verify_matt_plapp_shorts_quality.py

Verifies 100% compliance of knowledge/matt-plapp/matt-plapp-short-form/ dossiers:
- Proper lowercase kebab-case naming
- Valid taxonomy category
- Frontmatter completeness
- Required headings present
- Preserved numbers / calculations
- Valid source video link
"""

import glob
import os
import re
import sys

BASE_DIR = os.path.join("knowledge", "matt-plapp", "matt-plapp-short-form")

VALID_CATEGORIES = {
    "accounting", "analytics", "bar-beverage", "compliance", "cost-control",
    "customers", "delivery", "finance", "kitchen", "labour", "marketing",
    "menu", "operations", "ordering", "promotions", "technology"
}

REQUIRED_SECTIONS = [
    "# Key Information",
    "# Numbers / Calculations",
    "# Useful Method / Takeaway",
    "# Context",
    "# Source"
]

def verify_shorts():
    files = glob.glob(os.path.join(BASE_DIR, "**", "*.md"), recursive=True)
    print(f"Total shorts dossiers found: {len(files)}")
    assert len(files) == 1254, f"Expected exactly 1254 files, got {len(files)}"

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

        # Frontmatter check
        if not content.startswith("---"):
            errors.append(f"Missing frontmatter in {rel_path}")
            continue

        fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            errors.append(f"Malformed frontmatter in {rel_path}")
            continue

        fm_text = fm_match.group(1)
        if "serial:" not in fm_text or "title:" not in fm_text or "category:" not in fm_text or "tags:" not in fm_text:
            errors.append(f"Incomplete frontmatter keys in {rel_path}")

        # Check category match
        cat_match = re.search(r'category:\s*([a-z-]+)', fm_text)
        if not cat_match or cat_match.group(1) != cat_dir:
            errors.append(f"Category mismatch: folder={cat_dir}, fm={cat_match.group(1) if cat_match else 'None'} in {rel_path}")

        # Section check
        for sec in REQUIRED_SECTIONS:
            if sec not in content:
                errors.append(f"Missing required section '{sec}' in {rel_path}")

        # Numbers check
        nums_match = re.search(r'# Numbers / Calculations\s*\n(.*?)(?=\n#|$)', content, re.DOTALL)
        if not nums_match or not re.search(r'(\d+%|\$\d+|\d+)', nums_match.group(1)):
            errors.append(f"Missing numerical evidence in {rel_path}")

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
        print(f"SUCCESS: All {len(files)} Matt Plapp shorts dossiers passed 100% quality checks!")

if __name__ == "__main__":
    verify_shorts()
