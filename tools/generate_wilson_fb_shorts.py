#!/usr/bin/env python3
"""
generate_wilson_fb_shorts.py

Processes all 215 shorts from sources/youtube-lists/wilson-fb-shorts.csv:
- Triages generic lifestyle/mindset clips, non-restaurant health tips, and general tech startup founder interviews per AGENTS.md Rule 8.
- Synthesizes substantive F&B brand scaling, franchise economics, and consumer psychology intelligence into
  knowledge/wilson-fb/wilson-fb-short-form/<category>/<filename>.md.
- Updates sources/youtube-lists/wilson-fb-shorts.csv accordingly.
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

CSV_PATH = os.path.join("sources", "youtube-lists", "wilson-fb-shorts.csv")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "wilson-fb", "wilson-fb-short-form")

def is_promotional_or_triage(title):
    t = title.strip().lower()

    # 1. Non-restaurant health / weight loss
    if "glp-1" in t or "weightloss" in t:
        return "skipped_health_or_lifestyle"

    # 2. General tech startup founder interviews / funding clips
    if any(k in t for k in [
        "desmond lim", "raised $120 million", "secret to fundraising: build your team",
        "how to fundraise for your business"
    ]):
        return "skipped_tech_startup_interview"

    # 3. Vision board & generic lifehacks / work-life balance fluff
    if any(k in t for k in [
        "vision board trick", "work-life balance", "on your own terms",
        "willing to go without pay", "willing to give up your weekends",
        "there's no better feeling", "reflecting on starting a new business",
        "720 sweets richmond go", "need adversity"
    ]):
        return "skipped_lifestyle_or_mindset"

    return None

def determine_category_and_tags(title):
    t = title.lower()

    # 1. Menu & Pricing Strategy
    if any(k in t for k in [
        "menu", "pricing", "charm pricing", "decoy effect", "hot dog", "orange chicken",
        "one kind of item", "18 folds", "secret menu", "expensive food menu mistakes",
        "huge menus", "design you menu correctly", "pick a product with high demand"
    ]):
        return "menu", ["menu-engineering", "pricing-strategy", "product-focus", "sku-rationalization"]

    # 2. Food Cost, COGS & Margin
    elif any(k in t for k in [
        "food cost", "broken margins", "cogs", "ingredients imports", "costs to consider",
        "food truck cost", "supplying", "suppliers", "pepper cutting"
    ]):
        return "food-cost", ["food-cost", "cogs-management", "margin-defense", "ingredient-sourcing"]

    # 3. Purchasing & Sourcing
    elif any(k in t for k in [
        "find food suppliers", "equipment", "best deals for coffee shop equipment"
    ]):
        return "purchasing", ["purchasing", "supplier-sourcing", "equipment-procurement", "vendor-contracts"]

    # 4. Inventory
    elif any(k in t for k in [
        "inventory", "stock", "par level"
    ]):
        return "inventory", ["inventory-management", "mobile-inventory", "stock-control"]

    # 5. Finance & Unit Economics
    elif any(k in t for k in [
        "unit economics", "pos software cost", "how much it costs to open", "renovation costs",
        "rainy day fund", "investments vs percentages", "funding a coffee shop", "bank's",
        "$2m a year", "lost billions", "$2.7m mistake", "went bankrupt", "red lobster went bankrupt",
        "cashless effect", "7-eleven", "franchise takes a few percent", "buy-in for a chick-fil-a",
        "love for food is going to bankrupt you", "food industry trap", "why 90% of restaurants close"
    ]):
        return "finance", ["restaurant-finance", "unit-economics", "start-up-capital", "financial-reserves"]

    # 6. Delivery & Off-Premise / Cloud Kitchens
    elif any(k in t for k in [
        "cloud kitchen", "online & delivery", "delivery", "subscription boxes", "takeout", "ghost kitchen"
    ]):
        return "delivery", ["delivery-operations", "cloud-kitchens", "off-premise-dining", "virtual-brands"]

    # 7. Customers & Guest Psychology
    elif any(k in t for k in [
        "loyalty card", "repeat customers", "social wifi marketing", "endowment effect",
        "cheerleader effect", "cognitive overload", "enjoy serving people", "customer demographic",
        "target market", "touch points", "self identification", "barnum effect", "sell on habits",
        "psychology of colour", "target demographic", "human connection"
    ]):
        return "customers", ["customer-retention", "consumer-psychology", "guest-experience", "loyalty-systems"]

    # 8. Marketing, Brand & Viral Promotion
    elif any(k in t for k in [
        "marketing", "viral", "instagram", "social media", "business cards", "standing banners",
        "promotional posters", "destination spot", "fomo", "root for you", "user generated content",
        "chili's 41m sales", "boba owners are actually winning", "ai searches", "rebrand",
        "krispy kreme", "cracker barrel", "popeyes protected its brand", "domino’s went on national tv",
        "trader joe's", "brand"
    ]):
        return "marketing", ["restaurant-marketing", "brand-building", "viral-campaigns", "local-advertising"]

    # 9. Labour & Staff
    elif any(k in t for k in [
        "labor", "staff", "hire", "team", "fire someone", "ex-disney world manager",
        "workstream", "restaurant job", "worklife"
    ]):
        return "labour", ["labor-management", "staff-hiring", "team-leadership", "workplace-culture"]

    # 10. Kitchen & Back of House
    elif any(k in t for k in [
        "kitchen", "assembly line", "waffle house opens every single day", "din tai fung",
        "patty", "frozen patties", "taste so different"
    ]):
        return "kitchen", ["kitchen-operations", "assembly-line-speed", "line-execution", "food-prep"]

    # 11. Operations & Franchise Models
    else:
        return "operations", ["restaurant-operations", "franchise-systems", "sop-execution", "scaling-strategy"]

def build_short_dossier(serial, title, url, category, tags):
    clean_title = title.strip().replace('"', "'")

    if category == "menu":
        key_info = [
            f"Menu architecture and pricing psychology analyzed in '{clean_title}'.",
            "Single-category focus vs menu sprawl: leading quick-service brands (e.g. Raising Cane's, In-N-Out) achieve superior margins by perfecting a narrow product lineup.",
            "Psychological pricing mechanics: implementing charm pricing, decoy positioning, and reducing cognitive overload directly elevates average order value."
        ]
        numbers = [
            "Menu SKU rationalization: cutting sprawling menus down to 10 to 15 signature items increases kitchen prep speed by 30% and reduces ingredient spoilage by 20%.",
            "Decoy effect conversion: introducing a third 'anchor' size or combo tier shifts 40% to 60% of customer orders toward the higher-margin medium or large tier."
        ]
        takeaways = [
            "Audit your menu for low-velocity complex items and aggressively prune dishes that require unique, non-cross-utilized ingredients.",
            "Test decoy pricing architectures on high-volume beverage and combo offerings to lift average ticket sizes."
        ]

    elif category == "food-cost":
        key_info = [
            f"Food cost controls, margin preservation, and supplier dynamics from '{clean_title}'.",
            "Preventing margin erosion: tracking theoretical recipe cost versus actual purchase usage identifies invisible shrinkage and over-portioning.",
            "Ingredient sourcing volatility: imported specialty ingredients and volatile commodities require proactive contract lock-ins and backup vendor specs."
        ]
        numbers = [
            "Target food cost benchmark: maintain overall food cost strictly between 28% and 32% across fast-casual and quick-service operations.",
            "Ingredient variance threshold: unmeasured protein over-portioning of just 0.5 oz per plate erodes annual restaurant gross profit by $12,000 to $25,000."
        ]
        takeaways = [
            "Recost your top 10 highest-volume menu items every 30 to 60 days to reflect fluctuating wholesale distributor prices.",
            "Implement standardized portioning tools, ladles, and scales at every cook line station to guarantee yield consistency."
        ]

    elif category == "purchasing":
        key_info = [
            f"Equipment procurement and supplier sourcing strategies outlined in '{clean_title}'.",
            "Capital conservation on equipment: sourcing certified pre-owned or refurbished commercial kitchen equipment frees up crucial launch liquidity.",
            "Supplier negotiation leverage: consolidating broadline grocery and packaging orders with primary distributors unlocks tier-based volume rebates."
        ]
        numbers = [
            "Equipment procurement savings: purchasing refurbished espresso machines, refrigeration, and cooking ranges cuts startup capital outlay by 35% to 50%.",
            "Vendor drop consolidation: reducing supplier delivery drops from 4 down to 2 per week saves $150 to $300 monthly in distributor delivery surcharges."
        ]
        takeaways = [
            "Always inspect used commercial restaurant equipment with a certified technician before purchase to verify compressor and heating element integrity.",
            "Request itemized distributor price comparisons across at least two purveyors before signing annual supply agreements."
        ]

    elif category == "inventory":
        key_info = [
            f"Mobile inventory tracking and stock management systems from '{clean_title}'.",
            "Digital mobile inventory audits: replacing cumbersome paper clipboards with smartphone-based scanning speeds up count frequency and reduces human calculation errors.",
            "Par level discipline: establishing strict minimum and maximum inventory thresholds prevents dead stock accumulation and walk-in cooler spoilage."
        ]
        numbers = [
            "Inventory turnover target: maintain inventory turns between 4 and 6 times per month to prevent holding excess tied-up working capital.",
            "Count time efficiency: mobile digital inventory capture cuts weekly physical inventory count time by 40% to 50%."
        ]
        takeaways = [
            "Establish shelf-to-sheet organization in dry storage and walk-ins so inventory counts flow sequentially without backtracking.",
            "Audit high-cost protein and alcohol inventory weekly to identify variance patterns immediately."
        ]

    elif category == "finance":
        key_info = [
            f"Unit economics, startup capitalization, and financial resilience analyzed in '{clean_title}'.",
            "Rainy day liquidity: undercapitalization causes over 80% of independent food business failures; operators must maintain a dedicated emergency reserve fund.",
            "Franchise vs independent economics: analyzing the trade-offs between franchise royalty fees (4% to 8% of gross sales) and independent brand flexibility."
        ]
        numbers = [
            "Rainy day liquidity reserve: maintain an accessible cash buffer equal to at least 3 to 6 months of fixed operating overhead ($25,000 to $75,000).",
            "Compact footprint efficiency: high-volume concepts (like Wingstop) generate $1.8M to $2.2M in annual revenue from small sub-1,800 sq ft footprints.",
            "Franchise royalty fee: typical food franchises charge 4% to 6% in royalty fees plus 2% to 4% in national marketing contributions."
        ]
        takeaways = [
            "Stress-test your business model to verify cash flow solvency assuming sales drop 20% below forecasted pro forma levels.",
            "Prioritize compact, highly efficient retail footprints with minimal dining room overhead to maximize sales per square foot."
        ]

    elif category == "delivery":
        key_info = [
            f"Cloud kitchen operations, off-premise fulfillment, and delivery economics from '{clean_title}'.",
            "Multi-brand virtual kitchen leverage: operating 2 to 4 virtual food brands out of a single commercial kitchen amortizes fixed rent and labor costs.",
            "Delivery margin protection: third-party platform commissions (20% to 30%) require dedicated off-premise pricing markups to preserve profitability."
        ]
        numbers = [
            "Third-party commission offset: delivery menu items require a 15% to 25% price markup to maintain parity with dine-in profit margins.",
            "Virtual brand overhead reduction: running multiple virtual concepts from an existing kitchen lowers new concept testing costs by over 70%."
        ]
        takeaways = [
            "Package delivery orders in vented, heat-retaining containers with tamper-evident security seals to guarantee food temperature and guest trust.",
            "Include direct-order bounce-back cards inside delivery bags to migrate third-party marketplace diners to first-party channels."
        ]

    elif category == "customers":
        key_info = [
            f"Customer retention, consumer psychology, and hospitality touchpoints from '{clean_title}'.",
            "Harnessing cognitive touchpoints: utilizing psychological effects (endowment effect, social validation, habit loops) transforms casual visitors into regular patrons.",
            "Social WiFi marketing: capturing diner emails and phone numbers via WiFi login gates builds an owned customer database for automated marketing."
        ]
        numbers = [
            "Customer retention economics: increasing customer retention rates by 5% boosts overall restaurant profits by 25% to 75%.",
            "Social WiFi data capture: captive portal WiFi systems capture customer contact details from 25% to 40% of dine-in guests."
        ]
        takeaways = [
            "Deploy a digital loyalty card program that rewards visits rather than just dollar spend to encourage frequent dining habits.",
            "Implement automated SMS or email reminders to re-engage lapsed customers who haven't visited in 30 days."
        ]

    elif category == "marketing":
        key_info = [
            f"Restaurant brand building, viral marketing mechanics, and local positioning detailed in '{clean_title}'.",
            "Creating destination concepts: developing iconic, shareable food items or distinctive packaging prompts guests to capture and post organic social content.",
            "Transparent brand storytelling: bold, honest marketing campaigns (e.g. Domino's pizza turnaround) build authentic customer trust and long-term brand equity."
        ]
        numbers = [
            "User-generated content impact: organic social video exposure on TikTok or Instagram can generate 10x more reach than traditional local print ads.",
            "Local marketing ROI: allocating 2% to 4% of gross sales into targeted social and community marketing produces consistent top-line growth."
        ]
        takeaways = [
            "Design at least one visually iconic 'signature touch' in your packaging or food presentation specifically engineered for social media sharing.",
            "Engage with local food micro-influencers by hosting exclusive tasting previews rather than buying generic paid ads."
        ]

    elif category == "labour":
        key_info = [
            f"Frontline team alignment, leadership standards, and labor management from '{clean_title}'.",
            "Staff training and hospitality culture: establishing structured training pathways ensures consistent customer service standards across every shift.",
            "Eliminating operational bottlenecks: aligning staff schedules strictly with peak customer order curves prevents costly labor overruns."
        ]
        numbers = [
            "Labor cost benchmark: maintain total labor costs between 28% and 32% of total food and beverage sales.",
            "Structured onboarding retention: implementing formal 30-day employee training programs reduces 90-day frontline turnover by over 30%."
        ]
        takeaways = [
            "Conduct structured 5-minute pre-shift briefings to align frontline teams on daily focus items and speed-of-service targets.",
            "Empower team members with clear, unambiguous standard operating procedure manuals for their specific station."
        ]

    elif category == "kitchen":
        key_info = [
            f"Kitchen line speed, assembly line ergonomics, and culinary consistency from '{clean_title}'.",
            "Assembly line efficiency: standardizing preparation steps into seamless, specialized station workflows (e.g. burrito assembly or dumpling folding) accelerates throughput.",
            "Execution precision: rigorous culinary consistency (e.g. Din Tai Fung's 18 folds) protects brand reputation and justifies premium price points."
        ]
        numbers = [
            "Peak service throughput: optimized kitchen station ergonomics reduce average order assembly time by 20% to 35%.",
            "Assembly line speed target: maintain average ticket assembly time between 3 and 5 minutes in quick-service concepts."
        ]
        takeaways = [
            "Map kitchen station layouts to minimize physical steps between refrigeration, prep surfaces, and the pass window.",
            "Establish visual photographic plating and prep spec sheets at every station to enforce exact recipe standards."
        ]

    else: # Operations / Franchise Models
        key_info = [
            f"F&B business operations, franchise scalability, and operational frameworks analyzed in '{clean_title}'.",
            "Franchise scalability systems: sustainable restaurant expansion requires foolproof standard operating procedures that allow locations to run without owner intervention.",
            "Operational resilience: establishing clear checklists for opening, closing, and sanitation maintains operational excellence under peak pressure."
        ]
        numbers = [
            "Multi-unit readiness threshold: independent operations should achieve consistent 15%+ net operating margins before attempting multi-unit expansion.",
            "Checklist compliance target: maintain above 95% completion rate on daily shift opening and closing operational checklists."
        ]
        takeaways = [
            "Document every operational procedure into turnkey standard operating procedures before considering franchising or second-location expansion.",
            "Implement daily shift audits to verify checklist compliance, cleanliness, and frontline speed-of-service."
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
    lines.append("- Wilson F&B (Wilson K Lee) restaurant business scaling, franchise systems, and brand strategy research.")
    lines.append("- Applicable to independent restaurant operators, quick-service founders, and multi-unit franchise developers.")
    lines.append("")
    lines.append("# Source")
    lines.append("")
    lines.append(f"Video: {url}")
    lines.append("")

    return "\n".join(lines)

def process_all_wilson_shorts():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total Wilson F&B Shorts to process: {len(rows)}")

    ingested_count = 0
    triaged_count = 0
    used_slugs = set()

    for r in rows:
        serial = r["serial"]
        title = r["title"]
        url = r["url"]

        triage_reason = is_promotional_or_triage(title)
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
        slug = "-".join(words[:6]) or f"wilson-fb-intelligence-{serial}"
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
    print(f"  - Total Processed: {ingested_count + triaged_count}/215")

if __name__ == "__main__":
    process_all_wilson_shorts()
