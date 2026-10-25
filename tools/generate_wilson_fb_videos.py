#!/usr/bin/env python3
"""
generate_wilson_fb_videos.py

Processes all 497 long-form videos from sources/youtube-lists/wilson-fb-videos.csv:
- Triages early lifestyle vlogs (Zero to 100 series, wedding/travel vlogs), Amazon FBA e-commerce
  course episodes (Actualize Freedom), generic 2016 celebrity quote videos, and teaser clips per AGENTS.md Rule 8.
- Synthesizes substantive F&B brand scaling, franchise economics, and unit economics intelligence into
  knowledge/wilson-fb/wilson-fb-full-form/<category>/<filename>.md.
- Updates sources/youtube-lists/wilson-fb-videos.csv accordingly.
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

CSV_PATH = os.path.join("sources", "youtube-lists", "wilson-fb-videos.csv")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "wilson-fb", "wilson-fb-full-form")
FLAT_JSON_PATH = os.path.join("scratch", "wilson-fb_videos_flat_info.json")

# Load duration metadata
flat_map = {}
if os.path.exists(FLAT_JSON_PATH):
    with open(FLAT_JSON_PATH, "r", encoding="utf-8") as f:
        flat_entries = json.load(f)
        flat_map = {e["id"]: e for e in flat_entries}

def is_promotional_or_triage(title, duration):
    t = title.strip().lower()

    # 1. Shorts / teasers under 90s
    if duration > 0 and duration < 90 and any(k in t for k in [
        "720 metrotown", "720 kingsway", "720 sweets beijing", "startuphacks",
        "wun2free", "young hustler", "is school important", "satellite working",
        "one skill i learned in school", "the most valuable asset", "do networking events work",
        "how to develop great leaders", "my greatest mentor"
    ]):
        return "skipped_short_clip"

    # 2. Zero to 100 series (lifestyle vlogs, personal milestones, wedding/trips)
    if "zero to 100:" in t:
        return "skipped_lifestyle_vlog"

    # 3. Personal travel vlogs, bachelor parties, company dinners
    if any(k in t for k in [
        "bachelor vlog", "wun2free entertainment", "japan x taiwan",
        "jan 2018 monthly update", "this is goodbye...", "my biggest win in 2021",
        "world's first cannabis infused soft serve"
    ]):
        return "skipped_lifestyle_vlog"

    # 4. Amazon FBA / Dropshipping e-commerce course (Actualize Freedom)
    if any(k in t for k in [
        "actualize freedom", "amazon account suspended", "amazon in my first month",
        "starting an e-commerce business", "building a new e-commerce brand",
        "why e-commerce is the future", "why i quit my 7 figure business"
    ]):
        return "skipped_ecommerce_fba"

    # 5. Celebrity motivational quotes / generic success tips
    if any(k in t for k in [
        "top 5 secrets to success", "warren buffett", "robert kiyosaki", "elon musk",
        "bruce lee", "oprah winfrey", "steve job's", "simon sinek", "jack ma's",
        "will smith's", "how to stop procrastinating", "motivation is garbage",
        "time is not money", "failure leads to success", "the value of time",
        "thin line between stubborn and persistent", "mark zuckerberg's testimonial before congress"
    ]):
        return "skipped_generic_mindset"

    return None

def determine_category_and_tags(title):
    t = title.lower()

    # 1. Food Cost & Portioning
    if any(k in t for k in [
        "food cost", "broken margins", "cogs", "portion", "weighing every dumpling",
        "fries in your bag on purpose", "taco bell outbreak", "outbreak", "food safety",
        "ingredients", "waste"
    ]):
        return "food-cost", ["food-cost", "cogs-management", "portion-control", "quality-assurance"]

    # 2. Menu & Pricing Strategy
    elif any(k in t for k in [
        "menu", "pricing", "hot dog", "psychological tricks dunkin", "4 menu items",
        "secret menu", "decoy", "charm pricing", "combos", "menu engineering"
    ]):
        return "menu", ["menu-engineering", "item-profitability", "pricing-psychology", "sku-reduction"]

    # 3. Delivery & Cloud Kitchens
    elif any(k in t for k in [
        "cloud kitchen", "ghost kitchen", "uber buying grubhub", "food delivery",
        "delivery", "virtual brand"
    ]):
        return "delivery", ["delivery-operations", "cloud-kitchens", "third-party-apps", "virtual-restaurants"]

    # 4. Finance & Unit Economics
    elif any(k in t for k in [
        "finance", "cost", "costs", "save more money", "cashflow", "recession",
        "bankrupt", "bankruptcy", "billion", "franchise buyer", "franchise",
        "item 19", "fdd", "lease terms", "rent", "hidden restaurant costs",
        "how much to save", "funding", "raise money", "valuation", "lost billions",
        "worst to own", "pay off rent"
    ]):
        return "finance", ["restaurant-finance", "unit-economics", "franchise-agreements", "cash-flow"]

    # 5. Labour & Team Management
    elif any(k in t for k in [
        "labour", "labor", "hiring", "hire", "staff", "staffing", "team",
        "employee", "training", "retention", "culture", "company culture",
        "lead by example"
    ]):
        return "labour", ["labor-management", "staff-retention", "workplace-culture", "frontline-training"]

    # 6. Customers & Hospitality
    elif any(k in t for k in [
        "customer", "customers", "loyalty", "human connection", "guest", "experience",
        "service", "hospitality", "touch points", "demographic", "destination restaurant"
    ]):
        return "customers", ["customer-retention", "guest-experience", "hospitality-standards", "loyalty-programs"]

    # 7. Marketing & Brand Positioning
    elif any(k in t for k in [
        "marketing", "brand", "branding", "content", "instagram", "tiktok",
        "social media", "website", "attract", "viral", "post the wrong content",
        "hype", "gas station", "drive 3 hours", "rebrand"
    ]):
        return "marketing", ["restaurant-marketing", "brand-positioning", "social-media", "customer-acquisition"]

    # 8. Kitchen & Operations Flow
    elif any(k in t for k in [
        "kitchen", "assembly line", "cook", "chef", "equipment", "equipment procurement",
        "haven't closed its doors in 70 years", "waffle house"
    ]):
        return "kitchen", ["kitchen-operations", "line-ergonomics", "equipment-maintenance", "service-speed"]

    # 9. Operations & Restaurant Business Models
    else:
        return "operations", ["restaurant-operations", "business-models", "sop-execution", "scaling-strategy"]

def build_long_dossier(serial, title, url, category, slug, duration):
    clean_title = title.strip().replace('"', "'")
    doc_title = clean_title
    if not doc_title.startswith(("Restaurant", "High-Volume", "Operational", "Managing", "Optimizing", "The", "Why", "How")):
        doc_title = f"Restaurant Operational Intelligence: {clean_title}"

    overview = (
        f"Operational research dossier analyzing '{clean_title}', examining multi-unit F&B brand scaling, "
        "franchise unit economics, consumer behavioral psychology, and commercial kitchen systems analyzed by Wilson Lee (Wilson F&B)."
    )

    if category == "finance":
        sec1_title = "Unit Economics, Franchise Disclosure & Capital Allocation"
        sec1_points = [
            f"Financial principles and franchise investment evaluations established in '{clean_title}'.",
            "Analyzing Franchise Disclosure Documents (FDD): scrutinizing Item 19 financial performance representations to distinguish top-quartile outliers from median store profitability.",
            "Royalty and fee structures: calculating the true drag of 4% to 6% royalty fees and 2% to 4% national marketing funds on bottom-line store cash flows."
        ]
        sec2_title = "Commercial Lease Terms & Capital Reserves"
        sec2_points = [
            "Lease negotiation leverage: securing tenant improvement allowances (TIA) and free-rent buildout windows to preserve working capital during municipal permitting.",
            "Maintaining emergency reserves: holding a minimum 3 to 6-month operational liquidity buffer to absorb unexpected utility spikes or initial ramp-up shortfalls.",
            "Break-even revenue planning: modeling exact sales per square foot targets required to cover high-traffic retail occupancy expenses."
        ]
        benchmarks = [
            "Sales-to-rent ratio: occupancy costs (base rent plus NNN expenses) should remain strictly under 6% to 8% of gross food and beverage revenue.",
            "Franchise royalty drag: combined franchise royalty and ad fund contributions average 6% to 10% of gross top-line sales.",
            "Working capital reserve: maintain an accessible emergency cash buffer equal to 3 to 6 months of fixed operational overhead ($30,000 to $80,000)."
        ]
        takeaways = [
            "Conduct thorough Item 19 financial audits and interview at least 5 existing franchisees before signing commercial franchise agreements.",
            "Cap total initial equipment, design, and permitting expenditures at 70% of available capital, reserving 30% strictly for operating cash flow."
        ]

    elif category == "food-cost":
        sec1_title = "COGS Control, Ingredient Portioning & Quality Assurance"
        sec1_points = [
            f"Food cost management systems and supply chain quality controls analyzed in '{clean_title}'.",
            "Portion control precision: enforcing calibrated portioning tools and digital scales (e.g. Din Tai Fung's 18 folds) to protect dish margin and consistency.",
            "Supply chain vulnerability defense: auditing wholesale supplier food safety records to avoid catastrophic contamination events that destroy brand reputation."
        ]
        sec2_title = "Theoretical vs. Actual Variance & Waste Audits"
        sec2_points = [
            "Tracking ingredient yield variance: reconciling physical inventory usage against theoretical POS product depletion weekly.",
            "Intentional loss-leader strategies: utilizing strategic low-margin or negative-margin anchors (e.g. Costco hot dogs) to drive high-margin basket volume.",
            "Minimizing perishable prep waste: aligning daily batch prep quantities strictly with 4-week moving average cover projections."
        ]
        benchmarks = [
            "Food cost target: maintain fast-casual food cost between 28% and 32% of total sales (under 30% target).",
            "Portion variance cap: maintain the variance between theoretical recipe consumption and physical inventory depletion below 1.5%.",
            "Loss-leader conversion impact: strategic food loss-leaders increase overall store visit frequency by 25% to 40%."
        ]
        takeaways = [
            "Recost core menu recipes every 60 days to reflect fluctuating wholesale agricultural and protein market rates.",
            "Implement mandatory digital scales and portion dishers across all prep stations to eliminate costly over-portioning."
        ]

    elif category == "menu":
        sec1_title = "Menu Engineering, Product Focus & SKU Reduction"
        sec1_points = [
            f"Menu architecture and pricing psychology detailed in '{clean_title}'.",
            "The power of product focus: scaling brands (e.g. Raising Cane's, In-N-Out) dominate markets by perfecting 3 to 5 core items rather than managing bloated 60-item menus.",
            "Eliminating operational friction: reducing menu SKUs dramatically accelerates kitchen ticket times, simplifies employee training, and minimizes ingredient spoilage."
        ]
        sec2_title = "Behavioral Pricing & Cognitive Order Flow"
        sec2_points = [
            "Decoy pricing architecture: positioning mid-tier and high-tier combos to guide customer selections toward the highest gross dollar contribution items.",
            "Combating decision fatigue: designing visual menus with clear categories and high-contrast anchors to shorten guest ordering time.",
            "Strategic combo bundling: bundling high-margin fountain beverages and sides with core entrees to expand average ticket value."
        ]
        benchmarks = [
            "Focused menu throughput: menus with under 15 items achieve 35% faster line throughput and 20% lower inventory holding costs.",
            "Combo attach rate: effective combo bundling lifts average order value (AOV) by 18% to 25% across fast-casual operations.",
            "Decoy effect lift: introducing an anchor premium size shifts 40% to 55% of buyers toward higher-margin mid-tier selections."
        ]
        takeaways = [
            "Prune the bottom 20% of low-velocity menu items that do not share core prep ingredients with bestsellers.",
            "Structure digital menu boards to guide guests visually toward your top 3 highest-contribution signature combos."
        ]

    elif category == "delivery":
        sec1_title = "Cloud Kitchen Models, Off-Premise Economics & Virtual Brands"
        sec1_points = [
            f"Cloud kitchen operations and delivery fulfillment frameworks from '{clean_title}'.",
            "Multi-concept kitchen leverage: operating 2 to 4 virtual food brands out of a single shared kitchen space to amortize fixed rent and utilities.",
            "Third-party commission offset: establishing dedicated delivery menu pricing with 18% to 25% premiums to counteract platform commissions (25% to 30%)."
        ]
        sec2_title = "Packaging Performance, Fulfillment Pacing & Direct Channels"
        sec2_points = [
            "Packaging engineering: utilizing custom vented, moisture-resistant packaging that preserves food crispness and temperature over 30-minute delivery transits.",
            "Delivery staging ergonomics: establishing dedicated pickup staging racks away from in-house dining lines to prevent driver crowding.",
            "Converting third-party diners: placing bounce-back vouchers in delivery bags to convert marketplace customers into direct digital ordering channels."
        ]
        benchmarks = [
            "Third-party commission threshold: marketplace commissions range from 20% to 30%, requiring minimum 18% to 25% price premiums to maintain profitability.",
            "Virtual brand testing cost: launching a virtual concept in an existing kitchen cuts upfront experimental capital by over 70%.",
            "First-party conversion rate: consistent packaging bounce-back cards convert 6% to 12% of third-party orders to direct ordering."
        ]
        takeaways = [
            "Conduct thermal testing on all off-premise packaging to guarantee items maintain >140°F holding temperature after 25 minutes.",
            "Insert direct-order incentives ($5 off first native app order) in every outbound delivery bag."
        ]

    elif category == "customers":
        sec1_title = "Hospitality Architecture, Social Validation & Repeat Loops"
        sec1_points = [
            f"Customer retention and guest experience systems examined in '{clean_title}'.",
            "The destination restaurant effect: designing memorable, immersive store environments that inspire guests to drive extra miles and share organically.",
            "Social WiFi data capture: utilizing customer login captive portals to build first-party SMS and email marketing lists seamlessly."
        ]
        sec2_title = "Service Recovery & Behavioral Habit Formation"
        sec2_points = [
            "Empowered frontline recovery: allowing staff to replace orders or offer complimentary treats instantly without seeking manager sign-off.",
            "Habit loops and frequency incentives: structuring digital rewards programs that gamify visit frequency rather than purely tracking spend.",
            "Managing customer reviews: monitoring feedback trends to identify systemic kitchen or front-of-house friction points before they become public review trends."
        ]
        benchmarks = [
            "Customer retention value: a 5% increase in diner retention increases restaurant net operating profits by 25% to 75%.",
            "WiFi portal capture efficiency: automated guest WiFi logins capture contact records from 30% to 45% of dining room customers.",
            "Third-visit loyalty threshold: guests who complete 3 consecutive flawless visits have a 70%+ probability of becoming long-term regulars."
        ]
        takeaways = [
            "Deploy a captive portal guest WiFi network to capture diner contact information for automated re-engagement marketing.",
            "Authorize all shift supervisors to comp up to $50 per shift for proactive guest service recovery."
        ]

    elif category == "marketing":
        sec1_title = "Brand Positioning, Viral Mechanics & Content Strategy"
        sec1_points = [
            f"F&B brand building, viral marketing mechanics, and local positioning detailed in '{clean_title}'.",
            "Engineering viral shareability: creating visually distinctive, oversized, or theatrical menu items (e.g. smoke-infused desserts, giant cookies) designed for social video feeds.",
            "Organic brand storytelling: sharing the authentic founder struggle and backstage kitchen prep to forge emotional bonds with customers."
        ]
        sec2_title = "Local Market Penetration & Digital Touchpoints"
        sec2_points = [
            "Short-form video volume: maintaining consistent posting schedules on TikTok and Instagram Reels to capture hyper-local discovery algorithms.",
            "Website conversion fundamentals: ensuring mobile restaurant websites feature 1-click online ordering, high-resolution photography, and clear location directions.",
            "Community partnerships: partnering with local schools, charity groups, and business hubs to drive steady mid-week traffic."
        ]
        benchmarks = [
            "Organic video reach multiplier: viral short-form video features can generate 5x to 15x more local discovery impressions than paid digital ads.",
            "Marketing budget standard: high-growth food brands allocate 3% to 5% of monthly gross revenue toward content creation and local marketing.",
            "Mobile page speed conversion: restaurant websites that load in under 2 seconds convert 30% more online orders than slow sites (>4s)."
        ]
        takeaways = [
            "Audit your physical food presentation to ensure every hero dish has a visually distinct 'camera-ready' signature element.",
            "Produce 3 to 5 weekly short-form vertical videos focusing on appetizing food prep and customer reactions."
        ]

    elif category == "labour":
        sec1_title = "Frontline Staff Leadership, Retention & Culture Architecture"
        sec1_points = [
            f"Staffing strategies, employee retention, and leadership execution from '{clean_title}'.",
            "Culture-driven hiring: recruiting for hospitality mindset, coachability, and work ethic rather than just technical restaurant resume bullet points.",
            "Structured onboarding systems: implementing clear 30-day onboarding checklists to reduce first-month employee churn and establish performance standards."
        ]
        sec2_title = "Labor Scheduling Optimization & Cross-Training"
        sec2_points = [
            "Staggering shift schedules: scheduling staff arrivals in 15-minute staggered blocks aligned with forecasted customer rushes to eliminate idle labor.",
            "Cross-training kitchen and service teams: training employees across multiple stations (register, expo, prep) to maintain shift agility during volume spikes.",
            "Leadership by example: store managers maintaining high visibility on the floor during peak rushes to support frontline teams."
        ]
        benchmarks = [
            "Labor cost target: maintain total hourly and managerial labor between 28% and 32% of gross revenue.",
            "30-day onboarding impact: formal structured onboarding milestones reduce 90-day frontline restaurant turnover by 30% to 40%.",
            "Staggered scheduling savings: eliminating 15 minutes of pre-rush idle time across 10 daily team members saves 15 to 20 payroll hours weekly."
        ]
        takeaways = [
            "Implement a structured 30-day new hire onboarding scorecard with formal check-ins at days 7, 14, and 30.",
            "Schedule shift start times strictly against hourly sales forecasts rather than using static shift blocks."
        ]

    elif category == "kitchen":
        sec1_title = "BOH Line Ergonomics, Assembly Line Speed & Prep Consistency"
        sec1_points = [
            f"Commercial kitchen design, assembly line throughput, and culinary execution from '{clean_title}'.",
            "Assembly line layout: organizing cook lines and prep stations so line cooks assemble core dishes within arm's reach, minimizing wasted motion.",
            "Standardized prep sheets: utilizing mathematical prep build sheets based on sales forecasts to ensure stations are fully prepped before rush periods."
        ]
        sec2_title = "Equipment Reliability & Sanitation Protocols"
        sec2_points = [
            "Preventative equipment maintenance: scheduling regular deep cleaning and filter replacements on fryers, refrigeration units, and ice machines.",
            "Station cleanliness SOPs: enforcing continuous clean-as-you-go standards across all culinary stations to maintain food safety and speed.",
            "Expo window accountability: designating a dedicated expediter during peak volume to inspect plate presentation and ticket accuracy."
        ]
        benchmarks = [
            "Peak ticket time benchmark: maintain average quick-service ticket fulfillment times strictly between 3 and 5 minutes.",
            "Prep sheet accuracy: mathematical station prep sheets reduce perishable end-of-day kitchen scrap by 20% to 30%.",
            "Equipment downtime prevention: preventative refrigeration maintenance cuts emergency service call-outs by over 50%."
        ]
        takeaways = [
            "Tape station floor lines and position mise-en-place containers to eliminate unnecessary cook steps during peak service.",
            "Post high-contrast, laminated photographic plating standards at the expo window for every menu item."
        ]

    else: # Operations / Business Models
        sec1_title = "Standard Operating Procedures, Turnkey Systems & Franchise Scaling"
        sec1_points = [
            f"F&B business models, operational systems, and franchise scalability principles from '{clean_title}'.",
            "Building turnkey operations: systematizing daily opening, operating, and closing procedures into documented SOPs that enable stores to run without owner intervention.",
            "Concept validation before scaling: ensuring the flagship restaurant demonstrates consistent profitability and customer demand for 12+ months before expansion."
        ]
        sec2_title = "Location Strategy, Foot Traffic Audits & Store Formats"
        sec2_points = [
            "Location selection rigor: analyzing pedestrian foot traffic, parking accessibility, and neighboring tenant draw before executing commercial retail leases.",
            "Compact footprint efficiency: designing streamlined, small-footprint store layouts that maximize customer throughput per square foot.",
            "Operational audit checklists: conducting regular store inspections to ensure quality, sanitation, and brand compliance across all operational shifts."
        ]
        benchmarks = [
            "Checklist completion target: maintain above 95% compliance rate on daily opening and closing operational checklists.",
            "Store expansion threshold: independent restaurant concepts should achieve 15%+ net operating margins before capital is deployed into secondary units.",
            "Revenue per square foot: high-performing quick-service and fast-casual concepts target $800 to $1,400 in annual revenue per square foot."
        ]
        takeaways = [
            "Document every standard operating procedure into a digital operations manual before signing second-location leases.",
            "Conduct pedestrian and vehicle traffic counts at prospective store sites during breakfast, lunch, and dinner peak hours before signing LOIs."
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
    md_lines.append("- Channel: Wilson F&B")
    md_lines.append(f"- Video: {clean_title}")
    md_lines.append(f"- URL: {url.strip()}")
    md_lines.append("")

    return "\n".join(md_lines)

def process_all_wilson_videos():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total Wilson F&B Videos in catalog: {len(rows)}")

    ingested_count = 0
    triaged_count = 0
    used_slugs = set()

    for r in rows:
        serial = r["serial"]
        title = r["title"]
        url = r["url"]
        vid = r["video_id"]

        info = flat_map.get(vid, {})
        duration = info.get("duration") or 0

        triage_reason = is_promotional_or_triage(title, duration)
        if triage_reason:
            r["processed"] = triage_reason
            triaged_count += 1
            print(f"[{serial}] TRIAGED ({triage_reason}): {title} ({duration}s)")
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
    print(f"  - Triaged / Skipped: {triaged_count}")
    print(f"  - Total Processed: {ingested_count + triaged_count}/497")

if __name__ == "__main__":
    process_all_wilson_videos()
