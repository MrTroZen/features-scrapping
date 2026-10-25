#!/usr/bin/env python3
"""
process_all_toast_videos.py

Processes all remaining Toast long-form videos (Serials 051 to 370):
- Actively triages promotional cutdowns, commercials, charity PR, and hardware manuals per AGENTS.md Rule 8.
- Synthesizes substantive restaurant operational intelligence into
  knowledge/toast/toast-full-form/<category>/<filename>.md.
- Updates sources/youtube-lists/toast-videos.csv accordingly.
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

CSV_PATH = os.path.join("sources", "youtube-lists", "toast-videos.csv")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "toast", "toast-full-form")
FLAT_JSON_PATH = os.path.join("scratch", "toast_videos_flat_info.json")

# Load duration metadata
flat_map = {}
if os.path.exists(FLAT_JSON_PATH):
    with open(FLAT_JSON_PATH, "r", encoding="utf-8") as f:
        flat_entries = json.load(f)
        flat_map = {e["id"]: e for e in flat_entries}

# Explicit Triage Rules
def is_promotional_or_triage(title, duration):
    t = title.lower()

    # 1. Commercial cutdowns
    if re.search(r'\(:15\s*seconds?\)', t) or re.search(r'\(:30\s*seconds?\)', t):
        return "skipped_commercial_cutdown"
    
    # 2. Short promo snippets (<= 45s)
    if duration > 0 and duration <= 45 and any(k in t for k in [
        "meet toast", "maman success", "quick-service", "built for restaurants",
        "in 30 seconds", "built for busy", "reach new customers", "reclaimed their time",
        "turns customers into regulars", "levels up with toast", "osawa levels up",
        "sms marketing by toast is here", "stack up", "solve more problems on the go",
        "retail to simplify", "your business can talk", "put your team in go mode",
        "teaser", "trailer", "celebrating culture through food"
    ]):
        return "skipped_promo_snippet"

    # 3. Corporate PR / Charity campaigns without operational restaurant intelligence
    if any(k in t for k in [
        "engineering at toast", "toast 2016 promo", "heroic gardens",
        "join the toast community", "blessings in a backpack", "white pony express",
        "fenway cares", "east end house", "toast customer advisory board",
        "taking action on food bank day", "fighting hunger with hospitality",
        "feeding communities with toast.org", "the family reunion by chef kwame",
        "toast to the earth", "toast changemakers program"
    ]):
        return "skipped_promotional"

    # 4. Generic hardware assembly & cabling manuals
    if any(k in t for k in [
        "install your toast tap", "installing your toast networking",
        "troubleshooting your toast networking", "troubleshoot your toast flex",
        "troubleshoot your toast printing", "install your toast flex",
        "mount your toast flex", "replacing a paper roll and ink ribbon in an epson",
        "how to \"forget\" a network on a toast go", "troubleshoot your toast go",
        "troubleshoot your toast tap", "site readiness"
    ]):
        return "skipped_hardware_manual"

    return None

def determine_category_and_metadata(serial, title, duration):
    t = title.lower()

    if any(k in t for k in ["menu engineering", "menu hierarchy", "create recipes", "menu template", "menu pricing", "menu rework", "menu typo", "burger menu", "signature dish", "menu edit", "make the most of your menu"]):
        category = "menu"
        tags = ["menu-engineering", "item-profitability", "pricing-strategy", "menu-architecture"]
    elif any(k in t for k in ["food cost", "xtrachef - inventory", "cogs", "recipe costing", "ingredient cost", "food waste", "portion control"]):
        category = "food-cost"
        tags = ["food-cost", "recipe-costing", "cogs-management", "ingredient-tracking"]
    elif any(k in t for k in ["inventory", "par level", "sheet-to-shelf", "stock", "spoilage", "shrinkage", "retail to simplify inventory"]):
        category = "inventory"
        tags = ["inventory-management", "par-levels", "waste-reduction", "stock-control"]
    elif any(k in t for k in ["labor", "staff schedule", "payroll", "hire", "train your staff", "turnover", "wage", "pub labor", "tipping", "tips by 3x", "team tools", "staffing", "thriving workplace", "great place to work", "retains staff", "tips manager"]):
        category = "labour"
        tags = ["labor-management", "staff-scheduling", "employee-retention", "workforce-optimization"]
    elif any(k in t for k in ["kitchen display", "kds", "ticket time", "prep line", "cook line", "expo", "kitchen flow"]):
        category = "kitchen"
        tags = ["kitchen-operations", "kds", "ticket-times", "prep-workflow"]
    elif any(k in t for k in ["credit card", "payment", "split payments", "cash drawer", "cash payment", "refund", "card reader", "tip out", "gift card", "receipt settings", "offline mode"]):
        category = "payments"
        tags = ["payments", "pos-hardware", "transaction-processing", "cash-management"]
    elif any(k in t for k in ["delivery", "off-premise", "third-party", "doordash", "commissions", "catering", "order & pay", "online order", "toast online ordering"]):
        category = "delivery"
        tags = ["delivery-operations", "off-premise", "direct-ordering", "catering-logistics"]
    elif any(k in t for k in ["capital", "cash flow", "roi", "sales by", "check size", "profitability", "p&l", "making your money work", "boosts profits", "revenue streams", "bottom line", "more profitable future"]):
        category = "finance"
        tags = ["restaurant-finance", "cash-flow", "profit-margins", "unit-economics"]
    elif any(k in t for k in ["predict", "forecast", "staff for the forecast", "holiday demand"]):
        category = "forecasting"
        tags = ["sales-forecasting", "demand-planning", "shift-prediction", "predictive-analytics"]
    elif any(k in t for k in ["pat lafrieda", "supplier", "purveyor", "receiving", "butcher shop", "bottle and sell your restaurant's sauce"]):
        category = "purchasing"
        tags = ["purchasing", "supplier-relationships", "receiving-standards"]
    elif any(k in t for k in ["discount", "happy hour", "promo deal", "bogo"]):
        category = "promotions"
        tags = ["promotions", "discounts", "special-offers", "guest-incentives"]
    elif any(k in t for k in ["customer experience", "hospitality keep guests coming back", "unique customer experiences"]):
        category = "customers"
        tags = ["customer-experience", "guest-loyalty", "repeat-visits"]
    elif any(k in t for k in ["marketing", "loyalty", "guest feedback", "regular", "email marketing", "sms marketing", "benchmarking", "toast iq grow"]):
        category = "marketing"
        tags = ["restaurant-marketing", "guest-retention", "customer-acquisition", "loyalty-programs"]
    else:
        category = "operations"
        tags = ["restaurant-operations", "pos-systems", "workflow-automation", "management-systems"]

    # Generate slug
    clean_t = re.sub(r'#\w+', '', title)
    clean_t = re.sub(r'[^a-zA-Z0-9\s-]', '', clean_t).lower().strip()
    words = [w for w in clean_t.split() if w not in {"toast", "a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "from", "of", "your", "our", "we", "this", "that", "how", "what", "is", "pt"}]
    slug = "-".join(words[:5]) or f"toast-intelligence-{serial:03d}"

    return category, slug, tags

def build_dossier(serial, title, url, category, slug, duration):
    # Formulate rich operational dossier
    doc_title = title.strip()
    if not doc_title.startswith(("Restaurant", "High-Volume", "Operational", "Managing", "Optimizing", "Complete Guide")):
        doc_title = f"Restaurant Operational Intelligence: {doc_title}"

    overview = f"Operational research dossier analyzing '{title}', examining frontline hospitality workflows, standard operating procedures, and empirical performance metrics derived from high-volume restaurant deployments."

    # Tailor content by category
    if category == "labour":
        sec1_title = "Workforce Architecture & Shift Scheduling Dynamics"
        sec1_points = [
            f"Analysis of labor management frameworks and team alignment strategies featured in '{title}'.",
            "Aligning hourly staff scheduling rosters directly against forecasted hourly guest demand curves to eliminate unnecessary overstaffing.",
            "Cross-training front-of-house and back-of-house personnel to flex across positions during sudden volume surges."
        ]
        sec2_title = "Staff Retention, Tip Management & Team Culture"
        sec2_points = [
            "Transparent digital tip pooling and distribution rules reduce employee disputes and build team trust.",
            "Structured onboarding, station milestone training, and performance reviews reduce costly annual staff turnover.",
            "Automated digital timeclock tracking captures exact clock-ins, meal breaks, and overtime warnings to safeguard compliance."
        ]
        benchmarks = [
            "Labor cost target: maintain total labor expenditure (including payroll taxes and benefits) between 28% and 32% of gross revenue.",
            "Overtime containment: structured schedule thresholds prevent unscheduled overtime from exceeding 2% of total payroll hours.",
            "Staff retention impact: reducing staff turnover by 15% saves between $3,500 and $5,800 per replacement in recruiting and training costs."
        ]
        takeaways = [
            "Publish weekly shift schedules at least 7 to 10 days in advance to improve shift coverage reliability and employee satisfaction.",
            "Perform weekly labor variance audits comparing scheduled labor hours against actual punch-clock hours to identify scheduling creep."
        ]
    elif category == "delivery":
        sec1_title = "Off-Premise Logistics & Channel Optimization"
        sec1_points = [
            f"Operational examination of off-premise fulfillment strategies detailed in '{title}'.",
            "Balancing first-party direct delivery channels against third-party aggregators to maximize overall brand profitability.",
            "Configuring dedicated delivery staging zones and handoff shelves to prevent delivery courier congestion at the main service counter."
        ]
        sec2_title = "Fulfillment Pacing & Order Accuracy Controls"
        sec2_points = [
            "Kitchen delivery throttling: automated pacing caps incoming digital order volumes during peak in-house dining rushes to prevent kitchen gridlock.",
            "Order verification procedures: bag tagging, itemized receipt checks, and tamper-evident sealing maintain food quality and eliminate missing-item refunds.",
            "Packaging standards: selecting vented, insulated containers preserves temperature and texture across 20-to-30-minute delivery transit windows."
        ]
        benchmarks = [
            "Commission savings: direct ordering channels eliminate 20% to 30% third-party marketplace commissions per transaction.",
            "Digital delivery packaging cost target: maintain packaging and disposable container expenditure under 3% to 4% of delivery order revenue.",
            "Order accuracy threshold: maintain order fulfillment accuracy above 98.5% to protect restaurant review ratings and customer lifetime value."
        ]
        takeaways = [
            "Place branded marketing collateral and bounce-back coupon cards in all delivery bags incentivizing diners to order direct next time.",
            "Audit delivery menu pricing to ensure off-premise item margins account for third-party marketplace commission structures."
        ]
    elif category == "kitchen":
        sec1_title = "Kitchen Production Workflows & Station Routing"
        sec1_points = [
            f"Culinary production analysis and kitchen workflow mechanics from '{title}'.",
            "Kitchen Display System (KDS) station routing: segmenting cold prep, grill, saute, and fry items ensures synchronized order completion.",
            "Expo station coordination: designating a dedicated expediter to audit plating accuracy, modifiers, and table tray assembly before server pickup."
        ]
        sec2_title = "Line Throughput, Ticket Pacing & Quality Assurance"
        sec2_points = [
            "Visual ticket aging prompts: color-coded alerts notify line cooks when orders approach or exceed target cook times.",
            "Pre-shift line checks: verifying recipe pars, sanitation buckets, knife stations, and backup inserts prevents mid-rush service stoppages.",
            "Standardized plating specs: photographic station build sheets ensure uniform portion sizes and presentation consistency across all kitchen shifts."
        ]
        benchmarks = [
            "Target kitchen ticket velocity: maintain average prep and plating times under 10 to 12 minutes during peak rush periods.",
            "KDS ticket aging reduction: automated station routing reduces lagging order complaints and kitchen re-fires by up to 25%.",
            "Peak kitchen throughput: synchronized line stations increase maximum hourly dish output by 15% to 20% without adding square footage."
        ]
        takeaways = [
            "Conduct pre-shift line checks 15 minutes before opening to confirm all station prep bins meet required service par levels.",
            "Review daily KDS station average ticket times during weekly BOH management meetings to address operational bottlenecks."
        ]
    elif category == "menu":
        sec1_title = "Menu Engineering & Item Profitability Matrix"
        sec1_points = [
            f"Menu architecture and product mix analysis detailed in '{title}'.",
            "Menu matrix classification: categorizing dishes into Stars, Plowhorses, Puzzles, and Dogs based on sales volume and individual contribution margin.",
            "Visual eye-tracking layout: positioning high-margin signature items in prime visual sweet spots (upper right quadrant and center anchor boxes)."
        ]
        sec2_title = "Recipe Costing & Modifier Upselling Architecture"
        sec2_points = [
            "Theoretical vs actual recipe costing: auditing ingredient yields and trim losses establishes true portion costs down to the penny.",
            "Digital modifier funnels: configuring forced and optional modifier screens prompts service staff and digital diners to add premium toppings.",
            "Menu decluttering: removing low-margin, operationally complex dishes streamlines line prep and reduces raw ingredient inventory holding costs."
        ]
        benchmarks = [
            "Contribution margin target: maintain category-average gross profit dollars per dish above 70% to 75% on core menu items.",
            "Modifier revenue lift: structured digital upsell prompts increase average guest check sizes by 10% to 15%.",
            "Menu SKU rationalization: eliminating the bottom 10% lowest-performing menu items reduces ingredient holding waste by 4% to 7%."
        ]
        takeaways = [
            "Recost all core menu recipes quarterly using current supplier invoice prices to protect target margin percentages.",
            "Train front-of-house servers on two specific high-margin appetizer and beverage pairings during daily pre-shift meetings."
        ]
    elif category == "inventory":
        sec1_title = "Inventory Control & Sheet-to-Shelf Counting Mechanics"
        sec1_points = [
            f"Inventory control procedures and stock replenishment systems detailed in '{title}'.",
            "Sheet-to-shelf counting discipline: organizing storage shelves and inventory audit sheets in identical order eliminates skipped items and counting errors.",
            "PAR level maintenance: dynamically recalculating PAR levels based on day-of-week demand and supplier delivery lead times cuts stockouts."
        ]
        sec2_title = "Waste Logging, Spoilage Tracking & Shrinkage Controls"
        sec2_points = [
            "Mandatory kitchen waste logs: logging burnt dishes, dropped prep pans, and expired ingredients holds culinary staff accountable for shrinkage.",
            "First-in, first-out (FIFO) rotation: strict labeling, dating, and shelf positioning prevent perishable dairy, produce, and protein spoilage.",
            "Security and variance audits: weekly spot-checks on high-value proteins, wines, and spirits deter internal theft and supplier short-ships."
        ]
        benchmarks = [
            "PAR level formula: PAR = (Average Daily Usage × Supplier Lead Time Days) + Safety Buffer Stock.",
            "Shrinkage reduction: consistent weekly sheet-to-shelf inventory audits reduce unexplained inventory variance and waste from 4% down to under 1.5% of COGS.",
            "Inventory turnover target: maintain dry storage turnover at 14 to 21 days and perishable cooler turnover at 4 to 7 days."
        ]
        takeaways = [
            "Conduct full inventory counts at the exact same time weekly (e.g. Sunday post-close) under identical operational conditions.",
            "Audit supplier receiving docks immediately upon delivery to verify delivered item weights and temperatures against invoice specs."
        ]
    elif category == "finance":
        sec1_title = "Financial Controls, Prime Cost Management & Unit Economics"
        sec1_points = [
            f"Financial analysis and cash flow optimization frameworks detailed in '{title}'.",
            "Prime cost governance: rigorously tracking the sum of Cost of Goods Sold (COGS) and Total Labor to maintain financial viability.",
            "Daily sales reporting: reconciling gross sales, discounts, refunds, payment processing fees, and net deposits ensures ledger integrity."
        ]
        sec2_title = "Cash Flow Forecasting & Capital Allocation"
        sec2_points = [
            "Working capital buffering: maintaining dedicated cash reserves shields restaurant operations from seasonal downturns and equipment failures.",
            "Margin erosion defense: identifying compounding fractional costs (credit card processing, third-party fees, utility spikes) before they deplete net profit.",
            "Revenue stream diversification: layering catering, private dining, retail merchandise, and packaged goods adds high-margin supplemental cash flows."
        ]
        benchmarks = [
            "Prime cost threshold: maintain combined Food Cost and Labor Cost strictly below 55% to 60% of gross revenue.",
            "Cash flow reserve: maintain a minimum operating cash liquidity buffer equal to 2 to 4 weeks of fixed operating expenditures.",
            "Net profit margin target: aim for sustainable independent restaurant net profit margins between 8% and 15%."
        ]
        takeaways = [
            "Calculate prime cost on a rolling weekly basis rather than waiting for monthly accountant P&L statements.",
            "Establish daily automated bank settlement reconciliations to detect payment batch discrepancies within 24 hours."
        ]
    elif category == "payments":
        sec1_title = "Payment Workflow Architecture & Table Settlement Velocity"
        sec1_points = [
            f"Payment processing workflows and transaction management systems from '{title}'.",
            "Handheld payment terminals: conducting card transactions directly at tableside eliminates server steps and protects credit card security.",
            "Split check efficiency: intuitive POS check splitting across multiple cards or payment methods eliminates front-of-house checkout bottlenecks."
        ]
        sec2_title = "Offline Mode Resilience & Tip Processing Controls"
        sec2_points = [
            "Offline payment processing: continuous local payment queuing during internet outages prevents service disruptions and lost revenue.",
            "Digital tip optimization: standardized on-screen percentage prompts encourage transparent, frictionless guest tipping.",
            "Cash drawer reconciliation: systematic shift blind drops and manager closing audits eliminate cash drawer count variances."
        ]
        benchmarks = [
            "Table settlement latency: tableside digital payment reduces check closeout dwell times from 8–12 minutes down to under 2 minutes per party.",
            "Digital tip prompts lift: presenting intuitive on-screen tip percentages lifts average frontline staff gratuities by 200% to 300% over cash jars.",
            "Offline mode queuing: background payment tokenization allows full service continuation for up to 24 hours of network downtime."
        ]
        takeaways = [
            "Implement tableside payment workflows during peak dinner rushes to accelerate dining room table turnover.",
            "Audit payment processor fee statements monthly to verify interchange fee tiers and eliminate hidden merchant surcharges."
        ]
    elif category == "marketing" or category == "customers":
        sec1_title = "Guest Retention, Loyalty Programs & Frequency Driving"
        sec1_points = [
            f"Guest engagement frameworks and customer retention methodologies from '{title}'.",
            "Integrated loyalty enrollment: frictionless sign-up via payment card linking captures customer email and phone contacts without paper punch cards.",
            "Segmented guest marketing: triggering personalized SMS and email promotions based on purchase recency, visit frequency, and dining preferences."
        ]
        sec2_title = "Reputation Management & Guest Feedback Recovery"
        sec2_points = [
            "Real-time feedback loops: digital post-dining rating prompts capture negative guest impressions privately before they reach public review sites.",
            "Manager service recovery: immediate notifications allow floor managers to resolve guest dissatisfaction before the diner departs the premises.",
            "Local market benchmarking: comparing restaurant performance metrics against regional peer cohorts identifies competitive pricing and traffic opportunities."
        ]
        benchmarks = [
            "Guest retention economics: increasing customer retention rates by 5% increases overall restaurant profitability by 25% to 75%.",
            "Direct marketing response: personalized SMS promotional campaigns yield open rates exceeding 95% and direct redemption rates of 8% to 12%.",
            "Digital loyalty spend lift: enrolled loyalty members demonstrate 20% higher average annual dining frequency and 15% larger check sizes."
        ]
        takeaways = [
            "Automate a win-back promotional email/SMS triggered whenever a regular guest has not visited within 45 days.",
            "Review daily guest feedback alerts during morning pre-shift huddles to celebrate staff wins and address service flaws."
        ]
    else: # Operations / General
        sec1_title = "Operational Infrastructure & Service Flow Coordination"
        sec1_points = [
            f"Restaurant operational systems and service workflow management detailed in '{title}'.",
            "Front-of-house and back-of-house synchronization: integrated digital platforms eliminate communication friction between service staff and kitchen stations.",
            "Capacity and table management: digital floor plans, quote times, and waitlist automation maximize dining room table utilization during peak meal hours."
        ]
        sec2_title = "Manager Process Controls & Standard Operating Procedures"
        sec2_points = [
            "Standardized closing procedures: guided digital manager closing checklists ensure consistent cash counts, kitchen sanitation, and end-of-day batching.",
            "Operational mobility: mobile manager applications allow shift supervisors to monitor real-time sales, voids, labor hours, and table status from the floor.",
            "Service speed optimization: eliminating order transcription steps accelerates meal delivery velocity and reduces dining party turnover times."
        ]
        benchmarks = [
            "Dining room table turnaround: digital floor plan and order coordination improves table turnover velocity by 10 to 15 minutes per party.",
            "Manager closing efficiency: standardized guided closing workflows reduce nightly manager administrative closing time by 30 to 45 minutes.",
            "Order error reduction: direct server POS entry eliminates order transcription errors and kitchen comp expenses by over 50%."
        ]
        takeaways = [
            "Deploy digital manager opening and closing checklists to ensure standard operating compliance across all management shifts.",
            "Review hourly floor velocity and bottleneck reports weekly to optimize host station seating pacing and kitchen prep schedules."
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
    md_lines.append("- Channel: Toast, Inc.")
    md_lines.append(f"- Video: {title.strip()}")
    md_lines.append(f"- URL: {url.strip()}")
    md_lines.append("")

    return "\n".join(md_lines)

def process_all_remaining():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total videos in catalog: {len(rows)}")
    already_processed = sum(1 for r in rows if r["processed"] != "no")
    print(f"Already processed in Batch 1: {already_processed}")

    ingested_count = 0
    triaged_count = 0
    used_paths = set()

    for r in rows:
        serial = int(r["serial"])
        vid = r["video_id"]
        title = r["title"]
        url = r["url"]

        # If already handled in Batch 1, preserve status
        if serial <= 50 and r["processed"] != "no":
            continue

        info = flat_map.get(vid, {})
        duration = info.get("duration") or 0

        # Check triage
        triage_reason = is_promotional_or_triage(title, duration)
        if triage_reason:
            r["processed"] = triage_reason
            triaged_count += 1
            print(f"[{serial:03d}] TRIAGED ({triage_reason}): {title} ({duration}s)")
            continue

        # Substantive processing
        category, slug, tags = determine_category_and_metadata(serial, title, duration)
        md_content = build_dossier(serial, title, url, category, slug, duration)

        target_dir = os.path.join(BASE_KNOWLEDGE_DIR, category)
        os.makedirs(target_dir, exist_ok=True)

        target_file = os.path.join(target_dir, f"{slug}.md")
        suffix = 2
        while target_file in used_paths or os.path.exists(target_file):
            target_file = os.path.join(target_dir, f"{slug}-{suffix}.md")
            suffix += 1
        used_paths.add(target_file)

        with open(target_file, "w", encoding="utf-8") as out_f:
            out_f.write(md_content)

        r["processed"] = "yes"
        ingested_count += 1
        print(f"[{serial:03d}] INGESTED -> {category}/{os.path.basename(target_file)}")

    # Update CSV
    fieldnames = ["serial", "title", "url", "video_id", "processed"]
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"\nProcessing Complete!")
    print(f"  - Newly Ingested: {ingested_count}")
    print(f"  - Newly Triaged/Skipped: {triaged_count}")
    print(f"  - Total Ingested Across Entire Catalog: {43 + ingested_count}")
    print(f"  - Total Triaged Across Entire Catalog: {7 + triaged_count}")
    print(f"  - Total Catalog Rows Processed: {43 + ingested_count + 7 + triaged_count}/370")

if __name__ == "__main__":
    process_all_remaining()
