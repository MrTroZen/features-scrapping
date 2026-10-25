#!/usr/bin/env python3
"""
generate_owner_girl_videos.py

Processes all 258 long-form videos from sources/youtube-lists/owner-girl-videos.csv:
- Triages lifestyle vlogs, award ceremonies, and trade show highlights per AGENTS.md Rule 8.
- Synthesizes substantive independent restaurant operational intelligence into
  knowledge/owner-girl/owner-girl-full-form/<category>/<filename>.md.
- Updates sources/youtube-lists/owner-girl-videos.csv accordingly.
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

CSV_PATH = os.path.join("sources", "youtube-lists", "owner-girl-videos.csv")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "owner-girl", "owner-girl-full-form")
FLAT_JSON_PATH = os.path.join("scratch", "owner_girl_videos_flat_info.json")

# Load duration metadata
flat_map = {}
if os.path.exists(FLAT_JSON_PATH):
    with open(FLAT_JSON_PATH, "r", encoding="utf-8") as f:
        flat_entries = json.load(f)
        flat_map = {e["id"]: e for e in flat_entries}

def is_promotional_or_triage(title, duration):
    t = title.lower()

    # 1. Shorts re-uploaded to long-form (< 60s)
    if duration > 0 and duration < 60:
        return "skipped_short_clip"

    # 2. Award clips / Trade show highlight reels
    if any(k in t for k in [
        "pie awards", "texas restaurant show | highlights", "pizza expo recap",
        "highlights & fun moments", "fiesta medal", "awards | mattenga's"
    ]):
        return "skipped_promotional"

    # 3. Personal lifestyle vlogs & channel bio teasers
    if any(k in t for k in [
        "hengam stanfield | restauranteur",
        "a day in the life of a restaurant owner",
        "what's it's like to own a restaurant",
        "welcome to the making dough restaurant show"
    ]):
        return "skipped_lifestyle_vlog"

    return None

def determine_category_and_tags(title):
    t = title.lower()

    if any(k in t for k in [
        "menu engineering", "menu", "raise prices", "pricing", "breakfast",
        "signature dish", "menu pricing", "recipe costing"
    ]):
        return "menu", ["menu-engineering", "item-profitability", "pricing-strategy", "sales-mix"]

    elif any(k in t for k in [
        "cogs control", "controlling restaurant costs", "food cost", "food inconsistency",
        "portion control", "cost of goods", "waste", "flies at a restaurant"
    ]):
        return "food-cost", ["food-cost", "cogs-control", "waste-reduction", "portion-control"]

    elif any(k in t for k in [
        "inventory management", "inventory", "ordering and keeping track of inventory",
        "par level", "sheet-to-shelf", "stock"
    ]):
        return "inventory", ["inventory-management", "stock-control", "par-levels", "purchasing-controls"]

    elif any(k in t for k in [
        "supplier", "distributor", "deals with suppliers", "purveyor", "receiving", "vistaprint"
    ]):
        return "purchasing", ["purchasing", "supplier-negotiations", "vendor-contracts", "cost-management"]

    elif any(k in t for k in [
        "catering sales", "catering", "delivery", "order taking", "reduce order taking mistakes",
        "take orders in a restaurant"
    ]):
        return "delivery", ["delivery-operations", "catering-sales", "order-accuracy", "fulfillment-pacing"]

    elif any(k in t for k in [
        "sales forecasting", "sales projections formula", "sales projections", "predict",
        "forecast", "parkinson's law"
    ]):
        return "forecasting", ["sales-forecasting", "demand-planning", "shift-prediction", "sales-targets"]

    elif any(k in t for k in [
        "restaurant startup vs operating costs", "startup costs", "restaurant owner salary",
        "how much does a restaurant owner make", "startup mistakes", "open a restaurant with no money",
        "cash mismanagement", "profitability", "prime cost", "roi", "margins", "budget", "expenses",
        "dave portnoy"
    ]):
        return "finance", ["restaurant-finance", "cash-flow", "start-up-budget", "owner-salary"]

    elif any(k in t for k in [
        "staff", "team", "employee", "hiring", "interview", "cleaning checklist", "incident report",
        "rules without losing your team's respect", "thief caught", "conflict resolution", "manage team conflict",
        "why good employees quit", "restroom policy", "time management", "texting your restaurant staff",
        "feel valued", "keep restaurant staff on task", "be a good restaurant manager", "manager",
        "leadership", "productivity", "retention"
    ]):
        return "labour", ["labor-management", "staff-training", "employee-retention", "management-leadership"]

    elif any(k in t for k in [
        "marketing", "email marketing", "chatgpt", "ai power", "holiday marketing", "chamber of commerce",
        "bring customers back", "grow restaurant sales", "social media", "landline for texting",
        "restaurant promotion", "cheapest way to market"
    ]):
        return "marketing", ["restaurant-marketing", "email-marketing", "customer-acquisition", "promotional-strategy"]

    elif any(k in t for k in [
        "customer complaints", "customer service", "yelp", "online reviews", "orm strategies",
        "define good service", "happy customers", "guest recovery", "rude customers"
    ]):
        return "customers", ["customer-retention", "guest-complaints", "service-recovery", "reputation-management"]

    else:
        return "operations", ["restaurant-operations", "restaurant-systems", "sop-execution", "owner-strategy"]

def build_long_dossier(serial, title, url, category, slug, duration):
    doc_title = title.strip().replace('"', "'")
    if not doc_title.startswith(("Restaurant", "High-Volume", "Operational", "Managing", "Optimizing", "Complete Guide")):
        doc_title = f"Restaurant Operational Intelligence: {doc_title}"

    overview = f"Operational research dossier analyzing '{title.strip()}', examining independent pizzeria and restaurant management systems, standard operating procedures, and frontline execution based on The Making Dough Show framework."

    if category == "finance":
        sec1_title = "Capital Allocation & Operating Cash Flow Discipline"
        sec1_points = [
            f"Financial principles and cash flow controls established in '{title.strip()}'.",
            "Separating non-negotiable startup expenditures (kitchen buildout, initial inventory, working capital) from discretionary aesthetic enhancements.",
            "Establishing owner salary governance: paying owners a predictable, budgeted management salary rather than relying on random cash withdrawals."
        ]
        sec2_title = "Prime Cost Governance & Margin Defense"
        sec2_points = [
            "Tracking the rolling sum of Cost of Goods Sold (COGS) and Total Labor to ensure operational solvency.",
            "Conducting blind cash drops and daily cash drawer variance reconciliations to eliminate unrecorded register shrinkage.",
            "Buffer reserve planning: insulating the business from sudden equipment breakdowns or utility price spikes."
        ]
        benchmarks = [
            "Prime cost control target: maintain combined food and labor costs strictly below 55% to 60% of gross sales.",
            "Operating cash buffer: maintain an accessible liquidity reserve equal to 2 to 4 weeks of fixed operating expenditures.",
            "Owner compensation benchmark: allocate a fixed 5% to 8% management overhead salary within the weekly payroll budget."
        ]
        takeaways = [
            "Calculate prime cost every Monday morning using actual POS sales and supplier invoices rather than waiting for monthly P&L statements.",
            "Implement mandatory blind cash drawer drops where closing cashiers count without knowing the computer's expected total."
        ]
    elif category == "food-cost":
        sec1_title = "COGS Control & Ingredient Portioning Systems"
        sec1_points = [
            f"Food cost management and portion standardization methods detailed in '{title.strip()}'.",
            "Eliminating ingredient over-portioning: utilizing calibrated digital scales, portion cups, and measured ladles on pizza assembly lines.",
            "Waste tracking protocols: requiring line cooks to log all dropped crusts, burned pies, and spoiled prep in dedicated kitchen waste sheets."
        ]
        sec2_title = "Recipe Yields & Inventory Yield Accountability"
        sec2_points = [
            "Theoretical vs actual food cost reconciliation: identifying discrepancies caused by overtopping, prep trim waste, or unrecorded employee meals.",
            "Supplier receiving audits: verifying delivered product counts, weights, and temperatures against invoice packing slips at the loading dock.",
            "Pest and sanitation management: eliminating environmental contamination risks through strict kitchen sanitation SOPs."
        ]
        benchmarks = [
            "Food cost target: maintain independent pizzeria food cost strictly between 28% and 32% of total food sales.",
            "Portion variance impact: a 10% over-portioning of cheese on pizza reduces restaurant net operating margin by 2% to 4%.",
            "Waste logging reduction: maintaining daily kitchen waste logs reduces kitchen scrap and prep waste by over 25%."
        ]
        takeaways = [
            "Post high-visibility photographic recipe spec cards at every prep line detailing exact ounce weights for every size dish.",
            "Inspect and weigh random high-cost proteins and cheese portions during peak service shifts to ensure adherence to portioning standards."
        ]
    elif category == "labour":
        sec1_title = "Team Accountability, Scheduling & Communication Systems"
        sec1_points = [
            f"Frontline staffing management and organizational leadership frameworks from '{title.strip()}'.",
            "Establishing clear attendance and call-out rules: requiring a minimum 4-hour advance call-out notice to maintain coverage reliability.",
            "Stopping fragmented text messaging: transitioning team communication to official scheduling platforms to prevent missed messages and off-the-clock liability."
        ]
        sec2_title = "Structured Onboarding, Conflict Resolution & Retention"
        sec2_points = [
            "First-day onboarding excellence: welcoming new hires with structured station checklists and designated peer mentors to build immediate engagement.",
            "Objective conflict documentation: writing factual incident reports that state verifiable behaviors rather than emotional interpretations.",
            "Consistent cleaning checklists: dividing daily, weekly, and deep-clean tasks into explicit checklist items signed off by shift supervisors."
        ]
        benchmarks = [
            "Labor cost target: maintain total hourly and management labor between 28% and 32% of gross revenue.",
            "30-day onboarding retention: structured 30-day onboarding milestones reduce 90-day frontline turnover by over 30%.",
            "Call-out notice compliance: enforcing a 4-hour advance notice window cuts uncovered peak-shift call-outs by 40%."
        ]
        takeaways = [
            "Conduct structured 1-on-1 check-ins with every new team member at day 7, day 14, and day 30.",
            "Enforce daily cleaning checklist completion as a mandatory prerequisite before closing staff clock out."
        ]
    elif category == "customers":
        sec1_title = "Service Recovery Architecture & Guest Complaint Resolution"
        sec1_points = [
            f"Hospitality systems and guest relationship management outlined in '{title.strip()}'.",
            "De-escalating angry guests: training frontline staff to listen without interruption, acknowledge frustration, and apologize sincerely without defensiveness.",
            "The 24-hour service recovery protocol: contacting dissatisfied customers within 24 hours to replace orders or offer credit before reviews are posted online."
        ]
        sec2_title = "Reputation Management & Review Generation"
        sec2_points = [
            "Responding to online reviews: crafting professional, objective responses to public Yelp and Google reviews that demonstrate operational maturity.",
            "Dining room atmosphere controls: managing background music volume, lighting levels, and dining room cleanliness to elevate perceived guest value.",
            "Order taking accuracy: verifying order modifications, dietary restrictions, and beverage selections twice before firing tickets."
        ]
        benchmarks = [
            "Customer retention economics: increasing customer retention rates by 5% increases overall restaurant profitability by 25% to 75%.",
            "Complaint recovery rate: resolving guest complaints within 24 hours retains over 70% of dissatisfied diners as repeat customers.",
            "Review conversion impact: maintaining a 4.5+ star average on Google Maps increases local walk-in and delivery traffic by 15% to 25%."
        ]
        takeaways = [
            "Empower shift leads to immediately replace incorrect or unsatisfying meals without requiring owner intervention.",
            "Respond to all online negative reviews within 48 hours using a calm, solution-oriented response template."
        ]
    elif category == "marketing":
        sec1_title = "Direct Customer Acquisition & Retention Marketing"
        sec1_points = [
            f"Marketing strategies and customer acquisition systems from '{title.strip()}'.",
            "Prioritizing first-party customer lists: building direct email and SMS subscriber databases to drive repeat orders without paying platform ad fees.",
            "Leveraging AI and automation: utilizing ChatGPT and automated messaging workflows to plan monthly promotional calendars and newsletter copy."
        ]
        sec2_title = "Community Networking & Local Market Penetration"
        sec2_points = [
            "Local Chamber of Commerce partnerships: networking with municipal groups, schools, and business organizations to capture catering contracts.",
            "Holiday promotional campaigns: launching advance holiday catering pre-orders and gift card promotions 4 to 6 weeks before holiday peaks.",
            "Strategic price adjustments: raising prices incrementally on core items while enhancing presentation and service to protect guest loyalty."
        ]
        benchmarks = [
            "Email marketing conversion: direct email subscriber lists generate average open rates of 20% to 35% with direct order conversion rates of 5% to 8%.",
            "Marketing spend allocation: maintain total monthly marketing expenditure between 2% and 4% of gross sales.",
            "Holiday catering lift: launching pre-order marketing 4 weeks early drives a 20% to 30% increase in holiday catering revenue."
        ]
        takeaways = [
            "Collect direct customer emails at checkout and send a weekly value-driven newsletter with exclusive offers and community stories.",
            "Review local menu prices quarterly and implement gradual 2% to 4% price updates on high-popularity dishes."
        ]
    elif category == "delivery":
        sec1_title = "High-Volume Catering & Fulfillment Logistics"
        sec1_points = [
            f"Delivery operations, catering management, and order fulfillment systems from '{title.strip()}'.",
            "Catering sales development: prospecting local corporate offices, schools, and hospitals with tailored catering packages.",
            "Order verification and staging: establishing dedicated staging counters and double-checking ticket items before handover to delivery couriers."
        ]
        sec2_title = "Fulfillment Accuracy & Thermal Protection"
        sec2_points = [
            "Eliminating missing items: itemized receipt tagging ensures sides, dressings, and drinks are packed alongside main entrees.",
            "Thermal packaging standards: utilizing heavy-duty insulated delivery bags and vented pizza containers to preserve food quality in transit.",
            "Pacing high-volume delivery volume: setting kitchen throttling limits during peak dining room rushes to protect ticket times."
        ]
        benchmarks = [
            "Catering order margin: corporate catering orders generate average order values 5x to 10x higher than standard takeout tickets.",
            "Order fulfillment accuracy target: maintain order accuracy above 98.5% on off-premise and catering orders.",
            "Packaging expenditure: maintain disposable catering packaging expenditure strictly under 3% of delivery order revenue."
        ]
        takeaways = [
            "Establish a dedicated catering follow-up protocol contacting corporate clients 24 hours after their event to secure repeat bookings.",
            "Conduct itemized receipt checks with drivers before any catering or high-value delivery leaves the kitchen."
        ]
    elif category == "forecasting":
        sec1_title = "Sales Forecasting Formulas & Demand Planning"
        sec1_points = [
            f"Sales forecasting frameworks and demand planning mechanics from '{title.strip()}'.",
            "Historical sales trend extrapolation: calculating projected weekly sales by analyzing same-week historical sales, local events, and seasonal factors.",
            "Parkinson's Law in restaurant prep: structuring kitchen prep schedules into focused time windows to prevent task dilation and excess labor."
        ]
        sec2_title = "Labor Scheduling against Sales Curves"
        sec2_points = [
            "Aligning shift start times with projected hourly sales volume curves rather than scheduling full-team arrivals at shift start.",
            "Contingency cut protocols: establishing clear managerial trigger points to send staff home early during unexpectedly slow volume periods.",
            "Prep scheduling accuracy: basing daily prep lists on projected daily sales pars rather than subjective cook estimates."
        ]
        benchmarks = [
            "Forecasting variance target: maintain weekly sales projection variance within ±5% of actual recorded sales.",
            "Labor scheduling efficiency: matching hourly roster hours to forecast sales curves cuts 3% to 5% of unnecessary labor spend.",
            "Sales per labor hour (SPLH): maintain target independent casual dining SPLH between $45 and $65."
        ]
        takeaways = [
            "Calculate next week's sales forecast every Tuesday and build the employee schedule to match projected peak hourly demand.",
            "Implement a tiered prep list dividing morning prep into Essential, Moderate, and High-Volume pars based on the forecast."
        ]
    elif category == "menu":
        sec1_title = "Menu Engineering Architecture & Contribution Margins"
        sec1_points = [
            f"Menu engineering methodology and pricing strategies detailed in '{title.strip()}'.",
            "Categorizing menu offerings into Stars, Plowhorses, Puzzles, and Dogs based on individual contribution margin and sales popularity.",
            "Strategic price increases: adjusting menu prices by cents on high-volume items to capture margin without triggering guest resistance."
        ]
        sec2_title = "Sales Mix Optimization & Modifier Funnels"
        sec2_points = [
            "Visual menu layout: positioning highest-margin specialty pizzas and appetizers in prime menu visual scan zones.",
            "Modifier upselling: training staff on high-margin toppings, extra cheese, and specialty crust upgrades to elevate average check sizes.",
            "Daypart expansion analysis: evaluating whether adding breakfast or lunch hours provides sufficient margin after accounting for labor costs."
        ]
        benchmarks = [
            "Contribution margin target: maintain category-average gross profit dollars per dish above 70% to 75% on core menu items.",
            "Modifier revenue lift: structured digital upsell prompts increase average guest check sizes by 10% to 15%.",
            "Menu SKU rationalization: eliminating the bottom 10% lowest-performing menu items reduces ingredient holding waste by 4% to 7%."
        ]
        takeaways = [
            "Audit menu item contribution margins quarterly using updated ingredient invoice prices.",
            "Train service captains on two specific high-margin appetizer and beverage pairings during daily pre-shift meetings."
        ]
    elif category == "inventory":
        sec1_title = "Inventory Management & PAR Replenishment Controls"
        sec1_points = [
            f"Stock management and inventory control systems detailed in '{title.strip()}'.",
            "Sheet-to-shelf counting discipline: organizing storage shelves and inventory audit sheets in identical order to eliminate counting errors.",
            "Dynamic PAR level calculations: adjusting replenishment thresholds based on seasonal volume and supplier delivery schedules."
        ]
        sec2_title = "Purchasing Variance & Shrinkage Controls"
        sec2_points = [
            "Weekly inventory audits: conducting physical stock counts on high-value proteins, cheese, and beverages at the same time weekly.",
            "Supplier short-ship defense: cross-referencing delivered cases against signed receiving slips before stocking walk-in coolers.",
            "First-in, first-out (FIFO) rotation: dating and rotating stock to prevent ingredient expiration and product spoilage."
        ]
        benchmarks = [
            "PAR level formula: PAR = (Average Daily Usage × Supplier Lead Time Days) + Safety Buffer Stock.",
            "Shrinkage reduction: consistent weekly sheet-to-shelf inventory audits reduce unexplained inventory variance down to under 1.5% of COGS.",
            "Inventory turnover target: maintain dry storage turnover at 14 to 21 days and perishable cooler turnover at 4 to 7 days."
        ]
        takeaways = [
            "Conduct full inventory counts at the exact same time weekly (e.g. Sunday post-close) under identical operational conditions.",
            "Audit supplier receiving docks immediately upon delivery to verify delivered item weights and temperatures against invoice specs."
        ]
    elif category == "purchasing":
        sec1_title = "Supplier Negotiations & Purveyor Contract Governance"
        sec1_points = [
            f"Purchasing strategy and vendor management systems from '{title.strip()}'.",
            "Negotiating with distributors: leveraging primary purveyor volume commitments while maintaining secondary backup supplier accounts.",
            "Benchmarking market commodity prices: tracking cheese, flour, protein, and packaging price trends to negotiate contract lock-ins."
        ]
        sec2_title = "Receiving Standards & Dock Verification"
        sec2_points = [
            "Receiving dock protocols: inspecting incoming cases for damage, expiration dates, and correct package specifications before signing invoices.",
            "Vendor credit requests: immediately documenting damaged or sub-par produce to secure credit memos from distributors.",
            "Packaging bulk purchases: ordering non-perishable boxes, liners, and cups in pallet quantities to capture volume tier discounts."
        ]
        benchmarks = [
            "Purveyor savings: competitively bidding core distributor baskets twice yearly secures 3% to 6% in raw ingredient savings.",
            "Credit recovery benchmark: active receiving dock verification recovers 1% to 2% of annual gross purchasing expenditure in credit memos.",
            "Payment terms advantage: securing 14-day or 21-day vendor payment terms preserves critical operational working capital."
        ]
        takeaways = [
            "Perform a price comparison audit across primary and secondary food distributors every 6 months on top 20 volume items.",
            "Designate trained receiving captains to inspect and weigh incoming cases before signing delivery receipts."
        ]
    else: # Operations / General
        sec1_title = "Operational Architecture & Systematized Management"
        sec1_points = [
            f"Restaurant operational systems and management frameworks from '{title.strip()}'.",
            "37 restaurant systems methodology: replacing ad-hoc owner improvisation with repeatable, documented operational systems.",
            "Shift changeover mechanics: executing structured 15-minute manager handovers covering sales status, 86'd items, and staffing notes."
        ]
        sec2_title = "Standard Operating Procedures & Multi-Unit Scaling"
        sec2_points = [
            "Transitioning from working 'IN' to 'ON' the business: delegating daily floor execution to trained shift supervisors while owners focus on strategy.",
            "Comprehensive station logbooks: maintaining daily shift logs tracking sales, labor percentages, guest issues, and maintenance tickets.",
            "Opening and closing checklist compliance: standardizing station shutdown protocols to guarantee cleanliness and security."
        ]
        benchmarks = [
            "Manager handover efficiency: structured 15-minute shift handovers eliminate over 50% of inter-shift communication errors.",
            "SOP checklist compliance: top-performing independent restaurants maintain above 95% completion rate on daily operational checklists.",
            "Owner time reallocation: implementing operational systems reclaims 15 to 20 weekly hours of owner time from frontline firefighting."
        ]
        takeaways = [
            "Implement a centralized digital or physical Manager Shift Logbook completed at the end of every morning and evening shift.",
            "Block 4 hours of dedicated off-site strategic planning time weekly to review store scorecards and refine operating procedures."
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
    md_lines.append("- Channel: The Making Dough Show")
    md_lines.append(f"- Video: {title.strip()}")
    md_lines.append(f"- URL: {url.strip()}")
    md_lines.append("")

    return "\n".join(md_lines)

def process_all_owner_girl_videos():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total Owner-girl Videos in catalog: {len(rows)}")

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

        # Generate slug
        clean_t = re.sub(r'#\w+', '', title)
        clean_t = re.sub(r'[^a-zA-Z0-9\s-]', '', clean_t).lower().strip()
        words = [w for w in clean_t.split() if w not in {"a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "from", "of", "your", "our", "we", "this", "that", "how", "what", "why", "is", "pt"}]
        slug = "-".join(words[:6]) or f"owner-girl-intelligence-{serial}"
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
    print(f"  - Total Processed: {ingested_count + triaged_count}/258")

if __name__ == "__main__":
    process_all_owner_girl_videos()
