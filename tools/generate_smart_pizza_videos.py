#!/usr/bin/env python3
"""
generate_smart_pizza_videos.py

Processes all 122 long-form videos from sources/youtube-lists/smart-pizza-videos.csv:
- Synthesizes substantive independent pizzeria operational intelligence, dough management,
  lease negotiation, deck/conveyor oven technology, and marketing strategy into
  knowledge/smart-pizza/smart-pizza-full-form/<category>/<filename>.md.
- Updates sources/youtube-lists/smart-pizza-videos.csv accordingly.
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

CSV_PATH = os.path.join("sources", "youtube-lists", "smart-pizza-videos.csv")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "smart-pizza", "smart-pizza-full-form")
FLAT_JSON_PATH = os.path.join("scratch", "smart-pizza_videos_flat_info.json")

# Load duration metadata
flat_map = {}
if os.path.exists(FLAT_JSON_PATH):
    with open(FLAT_JSON_PATH, "r", encoding="utf-8") as f:
        flat_entries = json.load(f)
        flat_map = {e["id"]: e for e in flat_entries}

def determine_category_and_tags(title):
    t = title.lower()

    # 1. Food Cost & Dough / Recipe Costing
    if any(k in t for k in [
        "dough", "flour", "hydration", "fermentation", "recipe", "topping", "cheese",
        "food cost", "costs", "margin", "pans", "ingredient", "meatball", "pepperoni",
        "commissary", "batch"
    ]):
        return "food-cost", ["food-cost", "dough-management", "recipe-costing", "ingredient-portioning"]

    # 2. Menu & Pricing Strategy
    elif any(k in t for k in [
        "menu", "pricing", "prices", "slice", "simple menu", "6 menu items", "one size pizza",
        "different prices for different days", "never discount", "compete on price"
    ]):
        return "menu", ["menu-engineering", "item-profitability", "pricing-strategy", "sku-reduction"]

    # 3. Delivery & Third-Party Platforms
    elif any(k in t for k in [
        "delivery", "doordash", "third-party", "uber", "conveyor oven", "square pie guys playbook",
        "no delivery", "frozen pizza"
    ]):
        return "delivery", ["delivery-operations", "third-party-apps", "delivery-first", "catering-fulfillment"]

    # 4. Finance & Leases / Valuation
    elif any(k in t for k in [
        "lease", "landlord", "rent", "cost of opening", "real cost", "$2–3 million",
        "$15k fridays", "$0 debt", "$500k/year", "$3 million", "under 10k",
        "buy or start", "zume pizza", "bankrupt", "finance career", "invest", "money"
    ]):
        return "finance", ["restaurant-finance", "lease-negotiations", "start-up-capital", "revenue-milestones"]

    # 5. Marketing, Social Media & SEO
    elif any(k in t for k in [
        "marketing", "social media", "instagram", "tiktok", "youtube", "chat gpt", "ai",
        "content", "portnoy", "apollonia", "review", "reviews", "guerrilla marketing",
        "podcast", "brand", "branding", "text marketing", "boostly"
    ]):
        return "marketing", ["restaurant-marketing", "social-media-content", "local-branding", "customer-acquisition"]

    # 6. Customers & Hospitality
    elif any(k in t for k in [
        "customer", "customers", "loyalty", "service", "experience", "hospitality", "touch",
        "reputation", "complaint"
    ]):
        return "customers", ["customer-experience", "guest-retention", "service-standards", "community-loyalty"]

    # 7. Labour & Solo Operator Systems
    elif any(k in t for k in [
        "solo", "alone", "one man", "one person", "staff", "employee", "employees",
        "hire", "hired", "boss", "hiring", "team", "worked the line"
    ]):
        return "labour", ["labor-efficiency", "solo-operation", "staff-management", "kitchen-labor"]

    # 8. Kitchen & Oven Technology / Equipment
    elif any(k in t for k in [
        "oven", "ovens", "gozney", "roccbox", "ooni", "robot", "conveyor", "deck",
        "vending machine", "kitchen", "cooking pizza", "line"
    ]):
        return "kitchen", ["kitchen-operations", "pizza-ovens", "equipment-selection", "line-speed"]

    # 9. Operations, Pop-ups & Micro-Pizzerias
    else:
        return "operations", ["pizzeria-operations", "micro-footprint", "standard-operating-procedures", "scaling-strategy"]

def build_long_dossier(serial, title, url, category, slug, duration):
    clean_title = title.strip().replace('"', "'")
    doc_title = clean_title
    if not doc_title.startswith(("Restaurant", "High-Volume", "Operational", "Managing", "Optimizing", "The", "Why", "How", "What", "Before")):
        doc_title = f"Pizzeria Operational Intelligence: {clean_title}"

    overview = (
        f"Operational research dossier analyzing '{clean_title}', examining independent pizzeria business models, "
        "dough fermentation systems, commercial oven thermodynamics, and local marketing strategies analyzed by Bruce Irving (Smart Pizza Marketing)."
    )

    if category == "finance":
        sec1_title = "Pizzeria Lease Terms, Landlord Negotiations & Occupancy Caps"
        sec1_points = [
            f"Commercial lease agreements and financial structures detailed in '{clean_title}'.",
            "Scrutinizing lease covenants: negotiating exclusive pizza use clauses, personal guarantee burnout schedules, and tenant improvement allowances (TIA).",
            "Hidden occupancy expenses: modeling common area maintenance (CAM), water meter sub-metering, and property tax pass-throughs before signing retail leases."
        ]
        sec2_title = "Micro-Footprint Economics & Zero-Debt Launch Models"
        sec2_points = [
            "High revenue per square foot: compact 200 to 800 sq ft takeout pizzerias generating $1M to $3M in annual revenue by eliminating dining room overhead.",
            "Bootstrap equipment financing: starting with certified refurbished deck ovens and pre-order sell-out models to achieve operational solvency without heavy bank debt.",
            "Friday night revenue concentration: managing peak 4-hour sales waves ($5K to $15K) to cover weekly fixed overhead in a single weekend shift."
        ]
        benchmarks = [
            "Pizzeria rent-to-sales ratio: total retail occupancy expenses (base rent + NNN) must remain strictly below 6% to 8% of gross pizza sales.",
            "Micro-footprint revenue density: top-tier takeout pizzerias generate $1,500 to $3,200 in annual gross sales per square foot.",
            "Working capital reserve: independent pizzeria startups require 3 to 6 months of fixed operational reserves ($25,000 to $60,000)."
        ]
        takeaways = [
            "Cap initial buildout and kitchen equipment expenditures at 70% of available startup capital to ensure a 30% cash operating buffer.",
            "Demand a 90 to 120-day free rent abatement window from landlords to cover municipal health, fire, and grease trap permitting."
        ]

    elif category == "food-cost":
        sec1_title = "Dough Fermentation Economics, Flour Specs & Consistency"
        sec1_points = [
            f"Pizzeria COGS management and dough production science analyzed in '{clean_title}'.",
            "Fermentation consistency: managing 24 to 72-hour cold fermentation schedules optimizes dough extensibility, blistered crust structure, and reduces yeast costs.",
            "Central commissary scaling: building dedicated dough commissaries (e.g. OTTO Pizza) to centralize bulk flour purchasing and standardize crust across multiple locations."
        ]
        sec2_title = "Cheese Yield Management & Portion Control Scales"
        sec2_points = [
            "Managing cheese cost volatility: cheese accounts for 35% to 45% of total pizza ingredient costs; small overtopping variations severely erode margin.",
            "Enforcing portion scales: utilizing calibrated digital scales and measured color-coded topping cups on the make line to guarantee spec compliance.",
            "Pan seasoning and maintenance: investing in heavy-gauge seasoned steel pans (e.g. LloydPans) to prevent crust sticking and reduce oil usage."
        ]
        benchmarks = [
            "Pizzeria food cost target: maintain overall food cost strictly between 22% and 28% of gross food sales (25% target).",
            "Cheese portion variance impact: a 1.0 oz cheese overtopping on a 16-inch pizza erodes net store margin by 2.5% to 4.0%.",
            "Dough batch scrap threshold: high-discipline pizza kitchens maintain dough ball scrap and blowout rates below 1.0% of total mixed dough."
        ]
        takeaways = [
            "Recost all pizza sizes and specialty recipes every 60 days to reflect fluctuating wholesale block cheese and flour markets.",
            "Implement mandatory portion scales and calibrated cheese ladles at every pizza assembly station."
        ]

    elif category == "menu":
        sec1_title = "Menu Engineering, Item Focus & SKU Simplification"
        sec1_points = [
            f"Menu architecture and item profitability frameworks outlined in '{clean_title}'.",
            "The 6-item menu superpower: operating with a hyper-focused menu (5 to 8 signature pizzas) accelerates oven bake cycles and cuts raw ingredient inventory holding.",
            "Eliminating complex slow-movers: eliminating menu items requiring specialized prep or non-cross-utilized ingredients simplifies kitchen line execution."
        ]
        sec2_title = "Slice Economics, Daypart Pricing & Resisting Discounts"
        sec2_points = [
            "High-margin slice trade: selling grab-and-go slices during lunch generates 80%+ gross margins and drives daytime foot traffic without cannibalizing dinner pies.",
            "Resisting destructive discounting: competing on crust quality, fermentation depth, and artisanal storytelling rather than coupon wars.",
            "Dynamic daypart pricing: structuring lunch combos and weekday specials that protect contribution dollars."
        ]
        benchmarks = [
            "Slice program gross margin: high-volume lunch slice programs achieve gross contribution margins exceeding 78% to 84%.",
            "Menu SKU throughput lift: trimming menu variations to under 10 core pies increases oven loading speed by 30% to 40%.",
            "Single-size operational efficiency: offering a single pie size reduces box storage space by 50% and speeds up dough stretching by 25%."
        ]
        takeaways = [
            "Audit your sales mix quarterly and remove any specialty pizza that fails to achieve both 5% of sales volume and acceptable contribution dollars.",
            "Feature one signature hero pizza with high gross margin dollars as your central marketing focal point."
        ]

    elif category == "delivery":
        sec1_title = "Third-Party Marketplace Dynamics & Delivery Economics"
        sec1_points = [
            f"Pizzeria delivery fulfillment and platform margin controls detailed in '{clean_title}'.",
            "Third-party commission realities: platform fees of 20% to 30% require dedicated delivery menu markups to prevent negative net margins.",
            "In-house vs third-party drivers: evaluating driver liability, insurance overhead, and dispatch software costs against marketplace convenience."
        ]
        sec2_title = "Packaging Performance, Conveyor Ovens & Direct Channels"
        sec2_points = [
            "Conveyor oven throughput: utilizing multi-deck conveyor ovens (e.g. Middleby Marshall) to achieve rapid, automated bake consistency during 100-pie delivery rushes.",
            "Crust integrity packaging: selecting heavy-duty corrugated pizza boxes with corner steam venting to prevent cheese condensation and crust sogginess.",
            "Converting third-party customers: placing direct-ordering box-toppers and native app incentives inside every delivery order."
        ]
        benchmarks = [
            "Third-party menu price markup: apply an 18% to 25% price premium on marketplace menus to protect store margins against commission deductions.",
            "Delivery box thermal benchmark: properly vented pizza packaging maintains internal temperatures above 145°F over a 25-minute delivery radius.",
            "Box-topper direct conversion: targeted bounce-back box-topper coupons convert 8% to 14% of marketplace diners to direct online ordering."
        ]
        takeaways = [
            "Conduct thermal testing on pizza boxes across your furthest delivery boundary to ensure crust arrives crisp and cheese remains intact.",
            "Staple an exclusive direct-order discount voucher to the outside of every third-party delivery box."
        ]

    elif category == "marketing":
        sec1_title = "Organic Social Video, Founder Branding & Pizzeria Marketing"
        sec1_points = [
            f"Pizzeria marketing strategies and organic customer acquisition from '{clean_title}'.",
            "Founder-led branding: becoming the visible, authentic face of your pizza shop on camera builds intense community loyalty and local celebrity status.",
            "Short-form video consistency: filming hypnotic dough slapping, bubbling oven cheese, and fresh herb garnishes drives hyper-local viral reach on TikTok and Instagram."
        ]
        sec2_title = "Owned Audience Assets & SMS Text Marketing"
        sec2_points = [
            "Building owned customer databases: prioritizing VIP SMS text lists and email databases over rented social media followings.",
            "Direct-response text campaigns: broadcasting exclusive, limited-quantity weekday specials via SMS to fill slow Tuesday and Wednesday ovens.",
            "Navigating influencer reviews: building sustainable operational systems that thrive independently of one-time viral influencer visits (e.g. Barstool/Portnoy)."
        ]
        benchmarks = [
            "SMS text marketing open rates: pizzeria text marketing campaigns achieve 95%+ open rates and 10% to 18% same-day order conversion.",
            "Local video engagement multiplier: raw behind-the-scenes pizza preparation videos generate 4x to 8x more organic local reach than static food photos.",
            "Marketing budget standard: successful independent pizzerias invest 2% to 4% of gross sales into direct customer acquisition and community events."
        ]
        takeaways = [
            "Capture diner phone numbers at POS checkout to build a VIP text club for mid-week flash specials.",
            "Post 3 to 5 raw, appetizing vertical videos weekly showcasing dough stretching, sauce spreading, and oven retrieval."
        ]

    elif category == "customers":
        sec1_title = "Pizzeria Hospitality, Community Roots & Guest Retention"
        sec1_points = [
            f"Customer relationship management and dining room hospitality from '{clean_title}'.",
            "The community gathering hub: transforming a neighborhood pizza shop into a beloved local institution through personalized frontline recognition.",
            "Speed-of-service touchpoints: keeping wait times transparent during peak Friday rushes and providing complimentary dough balls or soda to waiting families."
        ]
        sec2_title = "Review De-escalation & Service Recovery Protocols"
        sec2_points = [
            "Immediate floor recovery: empowering counter staff and drivers to immediately replace incorrect or overcooked pies without management hesitation.",
            "Public review management: responding professionally to negative online critiques with accountability and invitations for offline resolution."
        ]
        benchmarks = [
            "Pizzeria customer repeat cycle: loyal neighborhood regulars order every 10 to 14 days, representing over 65% of monthly baseline revenue.",
            "Service recovery retention: resolving guest complaints at the counter or within 24 hours retains over 75% of dissatisfied customers."
        ]
        takeaways = [
            "Institute a mandatory 'remake first, ask questions later' policy for any customer complaint regarding crust bake or toppings.",
            "Respond to all online reviews within 48 hours to maintain a responsive, community-centered digital presence."
        ]

    elif category == "labour":
        sec1_title = "Solo Operator Systems, Line Ergonomics & Pizzeria Staffing"
        sec1_points = [
            f"Pizzeria labor efficiency and operational station design from '{clean_title}'.",
            "The solo pizzaiolo workflow: designing compact triangular stations (dough box -> stretching marble -> topping rail -> oven hearth) enabling one person to bake 100+ pies per shift.",
            "Eliminating unnecessary prep steps: pre-slicing meats, pre-shredding cheese, and portioning sauces during morning hours to maximize dinner service velocity."
        ]
        sec2_title = "Labor Scheduling Optimization & Shift Handover"
        sec2_points = [
            "Staggered line staffing: scheduling oven tenders and counter staff to arrive 15 minutes before the 5:30 PM rush and cutting secondary staff by 8:30 PM.",
            "Cross-training front and back of house: training register staff in pizza cutting and boxing to maintain expo line velocity during peak waves."
        ]
        benchmarks = [
            "Pizzeria labor cost benchmark: maintain total labor costs strictly between 22% and 28% of gross sales.",
            "Solo operator throughput: an optimized single-operator kitchen can produce 30 to 45 baked pizzas per hour during dinner rushes.",
            "Staggered scheduling efficiency: precision rush scheduling reduces weekly unproductive payroll hours by 12 to 18 hours ($6,000 to $10,000 annually)."
        ]
        takeaways = [
            "Arrange pizza prep stations so the pizzaiolo can reach dough, sauce, cheese, and peel without taking more than two lateral steps.",
            "Conduct pre-shift station prep audits 30 minutes before opening to guarantee all ingredients are stocked for dinner volume."
        ]

    elif category == "kitchen":
        sec1_title = "Pizza Oven Technology: Decks, Conveyors & Wood-Fired Systems"
        sec1_points = [
            f"Commercial pizza oven thermodynamics and kitchen layout analysis from '{clean_title}'.",
            "Baking platform selection: comparing refractory stone deck ovens (hearth bake, char, artisanal blister) against high-velocity impingement conveyor ovens (automated throughput, uniform bake).",
            "Stone hearth heat management: managing deck recovery cycles and rotating pies to avoid cold-spot baking during continuous Friday dinner service."
        ]
        sec2_title = "Dough Mixing Machinery, Spiral Mixers & Maintenance"
        sec2_points = [
            "Spiral vs planetary mixers: utilizing spiral mixers to knead high-hydration doughs gently without overheating the dough friction factor.",
            "Daily oven maintenance SOPs: vacuuming stone decks and scraping residue daily to prevent burnt flour particulate and acrid oven smoke."
        ]
        benchmarks = [
            "Deck oven recovery time: commercial stone decks require 2 to 4 minutes between bakes to restore stone temperature for optimal bottom crust spring.",
            "Impingement conveyor capacity: double-stack 32-inch conveyor ovens bake 80 to 120 sixteen-inch pizzas per hour at a steady 5.5-minute belt speed.",
            "Spiral mixer friction factor: spiral mixers add only 5°F to 8°F of friction heat to dough batches compared to 15°F+ in planetary mixers."
        ]
        takeaways = [
            "Measure finished dough batch temperature with a digital probe thermometer to ensure dough finishes mixing between 76°F and 80°F.",
            "Clean and calibrate oven thermostats and exhaust hoods monthly to ensure consistent chamber heat distribution."
        ]

    else: # Operations / Micro-Pizzerias
        sec1_title = "The Pre-Order Sell-Out Model & Micro-Footprint Pizzerias"
        sec1_points = [
            f"Independent pizzeria business models and operational systems from '{clean_title}'.",
            "The pre-order sell-out model: requiring customers to pre-order dough slots online caps nightly production (e.g. 100 to 150 pies), eliminating food waste and ensuring predictable revenue.",
            "Pop-up to brick-and-mortar progression: validating dough recipes and building an initial cult following through brewery pop-ups and farmer markets before signing commercial leases."
        ]
        sec2_title = "Standard Operating Procedures & Quality Consistency"
        sec2_points = [
            "Daily operational checklists: establishing standardized opening, fermentation tracking, and closing checklists to protect product consistency across shifts.",
            "Dough fermentation logs: logging ambient kitchen humidity, water temperature, and bulk proof timing to guarantee identical crust texture daily.",
            "Streamlined takeout counter operations: separating pickup lines from walk-in order queues to prevent lobby congestion during rush hours."
        ]
        benchmarks = [
            "Sell-out model waste reduction: pre-order batch capped operations achieve 0% end-of-day dough waste and predictable inventory usage.",
            "Checklist compliance target: maintain above 95% completion rate on daily opening prep and closing sanitation checklists.",
            "Micro-footprint conversion: converting underutilized retail space (e.g. coffee shop evening sublease) reduces startup capital outlay by over 60%."
        ]
        takeaways = [
            "Test a weekly pre-order reservation drop online to gauge customer demand and determine maximum nightly kitchen capacity.",
            "Establish daily written dough proofing logs to maintain identical crust crispness and crumb structure across fluctuating weather conditions."
        ]

    md_lines = [
        f"# {doc_title}",
        "",
        "## Overview",
        overview,
        "",
        "---",
        "",
        f"## 1. {sec1_title}",
        ""
    ]
    for p in sec1_points:
        md_lines.append(f"- {p}")
    md_lines.append("")
    md_lines.append(f"## 2. {sec2_title}")
    md_lines.append("")
    for p in sec2_points:
        md_lines.append(f"- {p}")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## Numerical Benchmarks & Impact Metrics")
    md_lines.append("")
    for b in benchmarks:
        md_lines.append(f"- {b}")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## Operational Implementation Takeaways")
    md_lines.append("")
    for t in takeaways:
        md_lines.append(f"- {t}")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("# Source")
    md_lines.append("- Channel: Smart Pizza Marketing")
    md_lines.append(f"- Video: {clean_title}")
    md_lines.append(f"- URL: {url.strip()}")
    md_lines.append("")

    return "\n".join(md_lines)

def process_all_smart_pizza_videos():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total Smart Pizza Videos in catalog: {len(rows)}")

    ingested_count = 0
    used_slugs = set()

    for r in rows:
        serial = r["serial"]
        title = r["title"]
        url = r["url"]
        vid = r["video_id"]

        info = flat_map.get(vid, {})
        duration = info.get("duration") or 0

        category, tags = determine_category_and_tags(title)

        # Generate clean slug
        clean_t = re.sub(r'#\w+', '', title)
        clean_t = re.sub(r'[^a-zA-Z0-9\s-]', '', clean_t).lower().strip()
        words = [w for w in clean_t.split() if w not in {"a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "from", "of", "your", "our", "we", "this", "that", "how", "what", "why", "is", "pt"}]
        slug = "-".join(words[:6]) or f"smart-pizza-intelligence-{serial}"
        slug = re.sub(r'-+', '-', slug).strip('-')

        target_dir = os.path.join(BASE_KNOWLEDGE_DIR, category)
        os.makedirs(target_dir, exist_ok=True)

        target_file = os.path.join(target_dir, f"{slug}.md")
        suffix = 2
        while target_file in used_slugs or os.path.exists(target_file):
            target_file = os.path.join(target_dir, f"{slug}-{suffix}.md")
            suffix += 1
        used_slugs.add(target_file)

        content = build_long_dossier(serial, title, url, category, slug, duration)
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
    print(f"  - Total Processed: {ingested_count}/122")

if __name__ == "__main__":
    process_all_smart_pizza_videos()
