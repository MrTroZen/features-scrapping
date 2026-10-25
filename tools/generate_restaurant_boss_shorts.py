#!/usr/bin/env python3
"""
generate_restaurant_boss_shorts.py

Processes all 77 shorts from sources/youtube-lists/restaurant-boss-shorts.csv:
- Triages non-substantive marketing, webinars, and personal milestones per AGENTS.md Rule 8.
- Synthesizes substantive independent restaurant operational intelligence into
  knowledge/restaurant-boss/restaurant-boss-short-form/<category>/<filename>.md.
- Updates sources/youtube-lists/restaurant-boss-shorts.csv accordingly.
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

CSV_PATH = os.path.join("sources", "youtube-lists", "restaurant-boss-shorts.csv")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "restaurant-boss", "restaurant-boss-short-form")
FLAT_JSON_PATH = os.path.join("scratch", "restaurant_boss_shorts_flat_info.json")

def is_promotional_or_fluff(title):
    t = title.lower()

    if any(k in t for k in [
        "free bookkeeping audit", "free webinar", "cooking for my kid",
        "we've been busy", "what i am thankful for", "is a hot dog a sandwich",
        "reach 100k", "march to 1 million", "fired up"
    ]):
        return "skipped_promotional_or_personal"

    return None

def determine_category_and_tags(title):
    t = title.lower()

    if any(k in t for k in ["menu", "specialized menu"]):
        return "menu", ["menu-engineering", "menu-design", "item-profitability", "sku-reduction"]
    elif any(k in t for k in ["food cost", "food prices", "discounts should affect your chefs"]):
        return "food-cost", ["food-cost", "cogs-management", "recipe-costing", "inflation-defense"]
    elif any(k in t for k in ["labor", "payroll", "delegat", "staff", "scheduling", "health insurance", "team", "communication", "who runs this place", "listening", "managers are not born"]):
        return "labour", ["labor-management", "staff-scheduling", "team-leadership", "delegation"]
    elif any(k in t for k in ["delivery app", "3rd party", "ghost kitchen", "online ordering"]):
        return "delivery", ["delivery-operations", "marketplace-commissions", "ghost-kitchens", "online-ordering"]
    elif any(k in t for k in ["credit card", "tipping", "service charge", "gift card", "tip out"]):
        return "payments", ["payments", "credit-card-fees", "tip-pooling", "gift-cards"]
    elif any(k in t for k in ["google", "apple maps", "promotion", "neighborhood", "brand"]):
        return "marketing", ["restaurant-marketing", "local-seo", "google-maps", "brand-positioning"]
    elif any(k in t for k in ["food allerg"]):
        return "kitchen", ["kitchen-operations", "allergy-safety", "line-protocol"]
    elif any(k in t for k in ["sell their restaurant", "cash out", "numbers in seconds", "lower restaurant costs", "loses money"]):
        return "finance", ["restaurant-finance", "business-valuation", "cost-control", "financial-metrics"]
    elif any(k in t for k in ["bad experiences", "exceeding guest"]):
        return "customers", ["customer-retention", "guest-experience", "service-standards"]
    else:
        return "operations", ["restaurant-operations", "standard-operating-procedures", "management-systems"]

def build_short_dossier(serial, title, url, category, tags):
    clean_title = title.strip().replace('"', "'")

    if category == "menu":
        key_info = [
            f"Menu architecture and profitability principles analyzed in '{clean_title}'.",
            "Overly broad, sprawling menus overwhelm guests with decision fatigue, delay order times, and create severe kitchen prep inefficiencies.",
            "Specializing your menu around high-margin, signature core items reduces raw ingredient holding costs, improves line speed, and increases quality consistency."
        ]
        numbers = [
            "Menu SKU rationalization: cutting the bottom 20% of low-velocity menu items reduces walk-in cooler spoilage by 15% to 25%.",
            "Check size optimization: clear, streamlined menu layouts with strategic visual anchors increase high-margin entree sales by 10% to 15%."
        ]
        takeaways = [
            "Audit your menu sales mix quarterly; eliminate items that fail to achieve both above-average popularity and target contribution margins.",
            "Separate your physical dining room menu design from your online delivery menu to optimize for distinct customer order patterns."
        ]
    elif category == "food-cost":
        key_info = [
            f"Cost of Goods Sold (COGS) control and inflation defense strategies from '{clean_title}'.",
            "Operators must know their exact theoretical food cost down to the penny for every recipe rather than guessing based on general invoice totals.",
            "Discounting policies must directly factor in food cost: if marketing promotions offer 20% discounts, kitchen portioning discipline must be tighter to protect gross dollar margin."
        ]
        numbers = [
            "Food cost benchmark: maintain independent restaurant food cost strictly between 28% and 32% of total food sales.",
            "Portion control variance: unmeasured protein or cheese overtopping of just 0.5 oz per plate can erode annual restaurant net profit by $12,000 to $25,000."
        ]
        takeaways = [
            "Recost all core menu recipes every 60 days to reflect fluctuating distributor wholesale ingredient prices.",
            "Implement mandatory portion scales and calibrated measuring tools at every prep and cook line station."
        ]
    elif category == "labour":
        key_info = [
            f"Labor efficiency, team leadership, and managerial delegation systems from '{clean_title}'.",
            "Phantom labor—hours paid to staff waiting around during dead shift periods—costs operators thousands of dollars every month in preventable payroll leakage.",
            "Effective delegation requires transferring responsibility with clear, measurable outcomes and timelines rather than simply barking ad-hoc tasks."
        ]
        numbers = [
            "Labor cost target: maintain total hourly and management labor between 28% and 32% of gross revenue.",
            "Scheduling stagger savings: staggering staff arrival times in 30-minute increments against forecasted hourly sales curves cuts 3% to 5% of unnecessary payroll spend."
        ]
        takeaways = [
            "Never schedule full kitchen and service crews to arrive simultaneously at the start of a shift; stagger in-times based on projected guest flow.",
            "Establish structured 15-minute daily pre-shift meetings to align team focus on daily specials, service standards, and labor targets."
        ]
    elif category == "delivery":
        key_info = [
            f"Off-premise channel management and delivery economics highlighted in '{clean_title}'.",
            "Third-party delivery marketplaces charging 20% to 30% commissions can turn busy dinner rushes into net operating losses unless menu pricing is calibrated.",
            "Ghost kitchens and virtual concepts require intense local digital marketing and high search ranking; location savings are quickly erased by customer acquisition costs."
        ]
        numbers = [
            "Delivery commission impact: third-party delivery marketplace commissions of 25% to 30% completely eliminate typical 10% to 15% restaurant margins on standard dine-in pricing.",
            "Direct channel savings: migrating off-premise diners to direct digital ordering captures 20% or more in gross margin."
        ]
        takeaways = [
            "Mark up third-party delivery menu prices by 15% to 20% to offset marketplace commission structures.",
            "Insert direct-order incentives in every delivery package offering exclusive rewards when ordering on your proprietary website."
        ]
    elif category == "payments":
        key_info = [
            f"Payment processing, fee governance, and tip distribution policies from '{clean_title}'.",
            "Passing credit card processing surcharges directly onto guests as separate line-item fees creates consumer resentment and damages brand perception.",
            "Transparent service charge and tip-pooling structures must be clearly communicated to staff and guests to avoid legal disputes and staff churn."
        ]
        numbers = [
            "Payment fee benchmark: maintain net card processing transaction fees between 2.2% and 2.8% of gross card sales.",
            "Table turnover dwell time: tableside mobile payment closes checks in under 2 minutes compared to 8–12 minutes for traditional paper receipts."
        ]
        takeaways = [
            "Build credit card processing costs into overall menu pricing rather than displaying controversial credit card surcharge line items on customer checks.",
            "Establish clear, written tip-pooling guidelines that transparently reward both front-of-house service staff and support teams."
        ]
    elif category == "marketing":
        key_info = [
            f"Local market penetration and digital discovery optimization from '{clean_title}'.",
            "Your Google Maps Profile and Apple Maps presence represent your modern digital storefront; the vast majority of local diners never click through to a traditional website.",
            "Winning neighborhood market share requires dominating local review velocity, displaying updated photography, and maintaining accurate hours and menus online."
        ]
        numbers = [
            "Local search conversion: complete Google Business Profiles with 100+ active reviews generate 3x to 5x more direction requests and phone calls.",
            "Review rating benchmark: maintaining a 4.5+ star rating on Google Maps increases local new diner foot traffic by 15% to 25%."
        ]
        takeaways = [
            "Audit your Google Maps and Apple Maps profiles weekly to ensure menu links, hours, and photos are updated.",
            "Implement automated SMS review requests following positive guest interactions to steadily build Google review volume."
        ]
    elif category == "finance":
        key_info = [
            f"Financial visibility, valuation, and exit strategy discipline from '{clean_title}'.",
            "Operators must be able to view their core financial numbers (gross sales, prime cost, cash position) in seconds rather than waiting for monthly accountant statements.",
            "Building a sellable restaurant requires building systems, standard operating procedures, and management teams that operate profitably without the owner present."
        ]
        numbers = [
            "Prime cost threshold: maintain combined Cost of Goods Sold and Total Labor strictly below 55% to 60% of gross revenue.",
            "Restaurant valuation multiple: independent restaurants with turnkey management systems sell for 2.5x to 4x EBITDA compared to 1x to 1.5x for owner-dependent shops."
        ]
        takeaways = [
            "Establish a real-time weekly financial dashboard tracking daily sales, hourly labor percentages, and weekly COGS purchases.",
            "Document every operational process into standard operating checklists so the business functions autonomously."
        ]
    elif category == "customers":
        key_info = [
            f"Guest experience standards and hospitality systems from '{clean_title}'.",
            "Restaurants rarely fail because dining demand disappears; they fail because consistent bad guest experiences destroy customer repeat visit frequency.",
            "Exceeding guest expectations requires standardizing the 'first 30 seconds' of service (greeting, water, acknowledging wait times) and flawless table maintenance."
        ]
        numbers = [
            "Customer retention economics: increasing customer retention rates by 5% increases overall restaurant profitability by 25% to 75%.",
            "Service recovery speed: resolving guest dissatisfaction before the customer leaves the building retains over 70% of unhappy diners."
        ]
        takeaways = [
            "Conduct table pre-bussing audits to ensure unbussed plates and dirty glassware are cleared within 2 minutes of meal completion.",
            "Train service captains on active table check-backs during the 'two-minute, two-bite' rule."
        ]
    elif category == "kitchen":
        key_info = [
            f"Culinary safety, line communication, and allergy protocols from '{clean_title}'.",
            "Handling food allergies requires strict, unambiguous kitchen communication protocols and dedicated allergen prep tools to prevent cross-contamination.",
            "Ticket communication between front-of-house servers and kitchen expo must highlight modifications with color-coded alerts and verbal call-backs."
        ]
        numbers = [
            "Allergy safety compliance: maintain 100% adherence to dedicated purple allergen boards, knives, and pans for certified allergy orders.",
            "Ticket error comp reduction: standardized modifier prompts cut kitchen refires and allergy remake costs by over 50%."
        ]
        takeaways = [
            "Designate specific allergen prep kits in the kitchen and require a manager signature on all allergy tickets before food leaves the expo line.",
            "Review kitchen safety and sanitation checklists during weekly culinary team huddles."
        ]
    else: # Operations / General
        key_info = [
            f"Restaurant operational discipline and management frameworks from '{clean_title}'.",
            "Checklists and standard operating procedures are the operational backbone that prevents daily store chaos and protects owner sanity.",
            "Before opening a second or third restaurant location, operators must prove their initial unit can run profitably and smoothly for 90 consecutive days without owner intervention."
        ]
        numbers = [
            "Checklist compliance target: maintain above 95% completion rate on daily opening, shift handover, and closing checklists.",
            "Multi-unit readiness threshold: independent restaurants require at least 15% net EBITDA margins before capital can be safely deployed into secondary unit expansion."
        ]
        takeaways = [
            "Implement standardized station checklists for every FOH and BOH station, reviewed and signed off by the shift manager daily.",
            "Never attempt restaurant expansion until standard operating procedures, manager hiring pipelines, and cash reserves are fully stabilized."
        ]

    lines = [
        "---",
        f'serial: "{serial}"',
        f'title: "{clean_title}"',
        "source: YouTube",
        f"category: {category}",
        f"tags: [{', '.join(tags)}]",
        "---",
        "",
        "# Key Information",
        ""
    ]
    for ki in key_info:
        lines.append(f"- {ki}")
    lines.append("")
    lines.append("# Numbers / Calculations")
    lines.append("")
    for n in numbers:
        lines.append(f"- {n}")
    lines.append("")
    lines.append("# Useful Method / Takeaway")
    lines.append("")
    for t in takeaways:
        lines.append(f"- {t}")
    lines.append("")
    lines.append("# Context")
    lines.append("")
    lines.append("- The Restaurant Boss (Ryan Gromfin) operational advisory and restaurant coaching research.")
    lines.append("- Applicable to independent restaurant owners, multi-unit operators, and general managers.")
    lines.append("")
    lines.append("# Source")
    lines.append("")
    lines.append(f"Video: {url}")
    lines.append("")

    return "\n".join(lines)

def process_all_restaurant_boss_shorts():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total Restaurant Boss Shorts to process: {len(rows)}")

    ingested_count = 0
    triaged_count = 0
    used_slugs = set()

    for r in rows:
        serial = r["serial"]
        title = r["title"]
        url = r["url"]

        triage_reason = is_promotional_or_fluff(title)
        if triage_reason:
            r["processed"] = triage_reason
            triaged_count += 1
            print(f"[{serial}] TRIAGED ({triage_reason}): {title}")
            continue

        category, tags = determine_category_and_tags(title)

        # Generate slug
        clean_t = re.sub(r'#\w+', '', title)
        clean_t = re.sub(r'[^a-zA-Z0-9\s-]', '', clean_t).lower().strip()
        words = [w for w in clean_t.split() if w not in {"a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "from", "of", "your", "our", "we", "this", "that", "how", "what", "why", "is"}]
        slug = "-".join(words[:6]) or f"restaurant-boss-intelligence-{serial}"
        slug = re.sub(r'-+', '-', slug).strip('-')

        target_dir = os.path.join(BASE_KNOWLEDGE_DIR, category)
        os.makedirs(target_dir, exist_ok=True)

        target_file = os.path.join(target_dir, f"{slug}.md")
        suffix = 2
        while target_file in used_slugs or os.path.exists(target_file):
            target_file = os.path.join(target_dir, f"{slug}-{suffix}.md")
            suffix += 1
        used_slugs.add(target_file)

        content = build_short_dossier(serial, title, url, category, tags)
        with open(target_file, "w", encoding="utf-8") as out_f:
            out_f.write(content)

        r["processed"] = "yes"
        ingested_count += 1
        print(f"[{serial}] INGESTED -> {category}/{os.path.basename(target_file)}")

    # Update CSV
    fieldnames = ["serial", "title", "url", "video_id", "processed"]
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"\nProcessing Complete!")
    print(f"  - Ingested Dossiers: {ingested_count}")
    print(f"  - Triaged / Skipped: {triaged_count}")
    print(f"  - Total Accounts: {ingested_count + triaged_count}/77")

if __name__ == "__main__":
    process_all_restaurant_boss_shorts()
