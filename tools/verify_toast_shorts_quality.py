#!/usr/bin/env python3
"""
verify_toast_shorts_quality.py

Runs quality-check on all 129 generated Toast short-form research files.
"""

import os
import re

BASE_DIR = os.path.join("knowledge", "toast", "toast-short-form")
VALID_CATEGORIES = {
    "finance", "food-cost", "labour", "inventory", "menu", "kitchen",
    "operations", "purchasing", "customers", "delivery", "payments",
    "forecasting", "marketing", "promotions", "social", "other"
}

errors = []
total_checked = 0

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if not f.endswith(".md"):
            continue
        total_checked += 1
        path = os.path.join(root, f)
        cat = os.path.basename(root)

        if cat not in VALID_CATEGORIES:
            errors.append(f"{path}: Invalid category '{cat}'")

        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        # Check frontmatter
        if not content.startswith("---\n"):
            errors.append(f"{path}: Missing YAML frontmatter start")
        m_serial = re.search(r'serial:\s*"(\d{3})"', content)
        if not m_serial:
            errors.append(f"{path}: Missing or invalid serial in frontmatter")

        # Check required sections
        if "# Key Information" not in content:
            errors.append(f"{path}: Missing # Key Information section")
        if "# Source" not in content:
            errors.append(f"{path}: Missing # Source section")
        if not re.search(r'# Source\s*\n\s*Video:\s*https?://', content):
            errors.append(f"{path}: Invalid or missing video link in # Source section")

        # Check product bloat forbidden terms
        forbidden = ["qavyo should build", "feature proposal", "backlog", "mvp recommendation", "feasibility score"]
        for term in forbidden:
            if term in content.lower():
                errors.append(f"{path}: Contains forbidden product bloat '{term}'")

if not errors:
    print(f"PASS: All {total_checked} Toast short-form research files passed 100% of quality checks!")
else:
    print(f"FAILED with {len(errors)} errors:")
    for e in errors[:10]:
        print(f"  - {e}")
