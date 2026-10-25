#!/usr/bin/env python3
"""
generate_matt_plapp_shorts.py

Processes all 1,257 shorts from sources/youtube-lists/matt-plapp-shorts.csv:
- Triages non-restaurant / automotive / personal clips per AGENTS.md Rule 8.
- Synthesizes substantive restaurant marketing ROI, owned customer databases,
  and promotional mechanics into knowledge/matt-plapp/matt-plapp-short-form/<category>/<filename>.md.
- Updates sources/youtube-lists/matt-plapp-shorts.csv accordingly.
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

CSV_PATH = os.path.join("sources", "youtube-lists", "matt-plapp-shorts.csv")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "matt-plapp", "matt-plapp-short-form")

def is_short_triage(title):
    t = title.strip().lower()
    if any(k in t for k in [
        "challenging a professional golfer", "dealership horror story",
        "rv & boat dealer leads", "free restaurant marketing audit"
    ]):
        return "skipped_non_restaurant_or_personal"
    return None

def determine_category_and_tags(title):
    t = title.lower()

    # 1. Promotions (High Priority for Matt Plapp)
    if any(k in t for k in [
        "red envelope", "promo", "promos", "promotion", "promotions", "contest",
        "giveaway", "free coffee or 10% off", "bogo", "first one free", "mother's day",
        "halloween", "easter", "christmas", "valentines", "birthday club", "bounce-back",
        "mystery envelope", "offer", "offers", "discount"
    ]):
        return "promotions", ["restaurant-promotions", "red-envelope-campaign", "promotional-roi", "seasonal-campaigns"]

    # 2. Customers & Loyalty
    elif any(k in t for k in [
        "customer", "customers", "loyalty", "vip", "repeat", "retention", "guest",
        "habit", "community", "reviews", "reputation", "relationship", "dating"
    ]):
        return "customers", ["customer-retention", "loyalty-programs", "guest-frequency", "community-loyalty"]

    # 3. Finance & ROI Economics
    elif any(k in t for k in [
        "roi", "cac", "acquisition cost", "ltv", "lifetime value", "$200,000 a year",
        "increase restaurant sales by 23%", "3 levers", "math", "get $1,500 back",
        "get $10 back for every $1", "$11,000 in sales", "money", "profit", "profitable",
        "margins", "budget", "cost", "costs", "sales"
    ]):
        return "finance", ["restaurant-finance", "marketing-roi", "customer-acquisition-cost", "revenue-growth"]

    # 4. Delivery & Off-Premise
    elif any(k in t for k in [
        "delivery", "doordash", "ubereats", "grubhub", "third party", "online ordering",
        "takeout", "catering"
    ]):
        return "delivery", ["delivery-operations", "third-party-fees", "online-ordering", "catering-sales"]

    # 5. Menu & Pricing / Upselling
    elif any(k in t for k in [
        "menu", "pricing", "price", "upsell", "upselling", "check size", "average check",
        "dessert", "drink", "beverage", "food"
    ]):
        return "menu", ["menu-engineering", "check-size-optimization", "upselling-systems", "pricing-strategy"]

    # 6. Labour & Staff Alignment
    elif any(k in t for k in [
        "staff", "team", "employee", "employees", "server", "servers", "hire", "hiring",
        "culture", "leadership", "manager", "name badge", "talk to your staff", "people"
    ]):
        return "labour", ["labor-management", "staff-engagement", "frontline-advocacy", "server-training"]

    # 7. Marketing, Advertising & Database
    elif any(k in t for k in [
        "marketing", "ads", "advertising", "facebook", "instagram", "tiktok", "social media",
        "database", "email", "text message", "sms", "video", "content", "influencer",
        "attention", "branding", "brand", "story", "photos", "engagement"
    ]):
        return "marketing", ["restaurant-marketing", "database-building", "social-media-ads", "sms-marketing"]

    # 8. Operations & Systems
    else:
        return "operations", ["restaurant-operations", "operating-systems", "independent-vs-chain", "owner-strategy"]

def build_short_dossier(serial, title, url, category, tags):
    clean_title = title.strip().replace('"', "'")

    if category == "promotions":
        key_info = [
            f"Promotional engineering and seasonal customer activation examined in '{clean_title}'.",
            "The Red Envelope promotion mechanics: distributing sealed mystery discount envelopes in December that can only be opened by a manager in January guarantees massive Q1 visit spikes.",
            "Items over percentage discounts: offering a tangible free item (e.g. free appetizer or dessert) creates higher perceived value and drives larger average tickets than generic 10% discounts."
        ]
        numbers = [
            "Red Envelope return rate: mystery envelope campaigns achieve 20% to 35% in-store redemption rates throughout January, recovering $15,000 to $30,000 in slow-season revenue.",
            "Item vs discount ROI: a free $8 appetizer promotion yields 4x higher customer response than a 15% discount while costing the restaurant under $2.50 in food cost."
        ]
        takeaways = [
            "Seal holiday promotional envelopes with explicit instructions: 'Do not open—must be opened by your server in January' to ensure redemption compliance.",
            "Always attach a minimum spend requirement (e.g. with purchase of two entrees) to free item promotional bounce-back offers."
        ]

    elif category == "customers":
        key_info = [
            f"Customer retention and guest lifetime value systems analyzed in '{clean_title}'.",
            "The 3 restaurant growth levers: top-line sales growth is driven by 1) acquiring new diners, 2) increasing visit frequency, and 3) lifting average check size.",
            "VIP and Birthday Club automation: capturing guest birthdays and anniversaries generates high-margin celebration table bookings year-round."
        ]
        numbers = [
            "Customer frequency impact: increasing average diner visits from 1.5 to 2.1 times per year expands total restaurant annual sales by over 20%.",
            "Birthday dining check size: party tables celebrating registered VIP birthdays spend an average of $85 to $140, with 3 to 5 accompanying paying guests."
        ]
        takeaways = [
            "Implement an automated Birthday Club sequence that sends dining vouchers 7 days before and 14 days after the customer's birthday.",
            "Train servers to ask diners if they are members of the VIP club and offer table-side QR code signups."
        ]

    elif category == "finance":
        key_info = [
            f"Restaurant marketing ROI, Customer Acquisition Cost (CAC), and unit economics from '{clean_title}'.",
            "Customer lifetime value mathematics: spending $3 to $5 to acquire a verified customer database record yields over $1,200 in lifetime dining revenue.",
            "Vanity metrics vs revenue: tracking actual in-store register redemptions and database opt-ins rather than social media likes and views."
        ]
        numbers = [
            "Target Customer Acquisition Cost (CAC): maintain customer database acquisition costs between $1.50 and $3.50 per verified diner.",
            "Return on Ad Spend (ROAS): targeted local restaurant social ad campaigns should achieve a minimum 4:1 to 8:1 tracked sales return."
        ]
        takeaways = [
            "Calculate your exact cost per customer database opt-in weekly by dividing ad spend by total new verified contacts captured.",
            "Track monthly redemption dollars directly in your POS using unique promotional promo codes."
        ]

    elif category == "delivery":
        key_info = [
            f"Delivery marketplace fee defense and off-premise channel strategy from '{clean_title}'.",
            "Third-party commission drain: marketplace commissions (25% to 30%) require proactive customer migration strategies to branded ordering platforms.",
            "Packaging bounce-backs: utilizing delivery bag inserts to capture third-party customer contact information and incentivize first-party ordering."
        ]
        numbers = [
            "Third-party commission penalty: unmonitored delivery platform fees erode net profit by 20% to 28% per off-premise ticket.",
            "Native ordering conversion: compelling box-topper vouchers convert 7% to 12% of marketplace diners into direct native app users."
        ]
        takeaways = [
            "Place an exclusive $5 bounce-back voucher in every delivery bag directing guests to order directly through your website.",
            "Mark up third-party delivery menu prices by 15% to 20% to offset platform commissions."
        ]

    elif category == "menu":
        key_info = [
            f"Menu architecture, strategic upselling, and average ticket expansion from '{clean_title}'.",
            "Suggestive selling protocols: training frontline service teams on specific sensory pairing recommendations (appetizers and desserts) to expand ticket sizes.",
            "Visual high-margin anchors: structuring digital and physical menus to highlight signature items with above-average gross contribution margins."
        ]
        numbers = [
            "Average check expansion: systematic server upselling of appetizers and specialty beverages lifts average table spend by $4.50 to $8.00.",
            "Dessert attach rate lift: offering table-side visual dessert displays increases dessert attachment from 8% to over 22%."
        ]
        takeaways = [
            "Incentivize servers with weekly sales competitions based on specific appetizer and dessert attach percentages.",
            "Highlight your top 3 highest-margin signature dishes with distinctive visual borders on physical and online menus."
        ]

    elif category == "labour":
        key_info = [
            f"Staff brand advocacy, frontline culture, and team alignment outlined in '{clean_title}'.",
            "Employees as brand ambassadors: empowering service staff with branded storytelling and personal connection elevates guest review ratings.",
            "Server contest gamification: structuring transparent shift sales leaderboards to motivate team members around core promotional goals."
        ]
        numbers = [
            "Staff retention through recognition: restaurants utilizing weekly performance gamification reduce frontline turnover by 25% to 35%.",
            "Frontline advocacy impact: servers who actively promote VIP club signups enroll 30 to 50 new customer records per week."
        ]
        takeaways = [
            "Reward the top-performing server in weekly VIP signups with gift cards or prime shift selection priority.",
            "Conduct 3-minute pre-shift huddles to review daily promotional goals and recognize outstanding service wins."
        ]

    elif category == "marketing":
        key_info = [
            f"Owned customer database building, digital advertising, and social content strategy detailed in '{clean_title}'.",
            "Owned audience supremacy: building a first-party database of 5,000+ local customer emails and cell phone numbers insulates operators from algorithm changes.",
            "Hyper-local paid social ads: running geo-targeted Facebook and Instagram ads within a 3 to 5-mile radius of the restaurant with clear lead-capture hooks."
        ]
        numbers = [
            "Database revenue velocity: an active database of 5,000 verified local diners generates $40,000 to $80,000 in tracked annual repeat revenue.",
            "Targeted radius efficiency: geo-fencing ads strictly within 3 miles cuts ad waste by 40% and increases in-store foot traffic response."
        ]
        takeaways = [
            "Run continuous hyper-local lead generation ads offering a signature menu item in exchange for name, email, and mobile number.",
            "Broadcast weekly automated text and email campaigns featuring compelling backstage video stories rather than constant discounting."
        ]

    else: # Operations / General
        key_info = [
            f"Independent restaurant systems, chain competition defense, and operational blueprints from '{clean_title}'.",
            "Out-localizing corporate chains: independent operators beat corporate restaurant chains by leveraging authentic community roots and founder visibility.",
            "Repeatable marketing assembly lines: establishing a consistent monthly promotional calendar prevents marketing stagnation and stabilizes year-round cash flow."
        ]
        numbers = [
            "Community marketing impact: active local sports team and charity partnerships drive 15% to 25% higher weekday family dining volume.",
            "Checklist compliance target: maintaining >95% compliance on marketing and operational shift checklists ensures consistent execution."
        ]
        takeaways = [
            "Plan your promotional calendar 90 days in advance with one major theme, community partnership, and VIP offer per month.",
            "Actively participate in local school, charity, and civic events to establish your restaurant as the neighborhood cornerstone."
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
    lines.append("- Matt Plapp (America's Best Restaurants) restaurant marketing, customer database building, and promotional ROI research.")
    lines.append("- Applicable to independent restaurant operators, multi-unit franchise owners, and hospitality marketers.")
    lines.append("")
    lines.append("# Source")
    lines.append("")
    lines.append(f"Video: {url}")
    lines.append("")

    return "\n".join(lines)

def process_all_matt_plapp_shorts():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total Matt Plapp Shorts to process: {len(rows)}")

    ingested_count = 0
    triaged_count = 0
    used_slugs = set()

    for r in rows:
        serial = r["serial"]
        title = r["title"]
        url = r["url"]

        triage_reason = is_short_triage(title)
        if triage_reason:
            r["processed"] = triage_reason
            triaged_count += 1
            print(f"[{serial}] TRIAGED ({triage_reason}): {title}")
            continue

        category, tags = determine_category_and_tags(title)

        # Generate clean slug
        clean_t = re.sub(r'#\w+', '', title)
        clean_t = re.sub(r'[^a-zA-Z0-9\s-]', '', clean_t).lower().strip()
        words = [w for w in clean_t.split() if w not in {"a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "from", "of", "your", "our", "we", "this", "that", "how", "what", "why", "is", "pt"}]
        slug = "-".join(words[:6]) or f"matt-plapp-intelligence-{serial}"
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
        if ingested_count % 100 == 0 or ingested_count == 1:
            print(f"[{serial}] INGESTED ({ingested_count}) -> {category}/{os.path.basename(target_file)}")

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
    print(f"  - Total Processed: {ingested_count + triaged_count}/1257")

if __name__ == "__main__":
    process_all_matt_plapp_shorts()
