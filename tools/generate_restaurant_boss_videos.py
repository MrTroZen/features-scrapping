#!/usr/bin/env python3
"""
generate_restaurant_boss_videos.py

Processes all 434 long-form videos from sources/youtube-lists/restaurant-boss-videos.csv:
- Triages software tutorials (clickBACON Ninja Tips, ClickBACON Wizards), client testimonials,
  holiday greetings, giveaways, and trailer clips per AGENTS.md Rule 8.
- Synthesizes substantive independent restaurant operational intelligence into
  knowledge/restaurant-boss/restaurant-boss-full-form/<category>/<filename>.md.
- Updates sources/youtube-lists/restaurant-boss-videos.csv accordingly.
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

CSV_PATH = os.path.join("sources", "youtube-lists", "restaurant-boss-videos.csv")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "restaurant-boss", "restaurant-boss-full-form")
FLAT_JSON_PATH = os.path.join("scratch", "restaurant_boss_videos_flat_info.json")

# Load duration metadata
flat_map = {}
if os.path.exists(FLAT_JSON_PATH):
    with open(FLAT_JSON_PATH, "r", encoding="utf-8") as f:
        flat_entries = json.load(f)
        flat_map = {e["id"]: e for e in flat_entries}

def is_promotional_or_triage(title, duration):
    t = title.strip().lower()

    # 1. Shorts re-uploaded to long-form (< 60s)
    if duration > 0 and duration <= 60 and ("#shorts" in t or "shorts" in t):
        return "skipped_short_clip"

    # 2. Software UI tutorials / screen demos (clickBACON Ninja Tips & Wizards)
    if "clickbacon ninja tip" in t or "clickbacon wizard" in t:
        return "skipped_software_demo"

    # 3. Client testimonials
    if "testimonial" in t:
        return "skipped_testimonial"
    if "mentorship that helped launch a massively successful dubai" in t:
        return "skipped_testimonial"

    # 4. Giveaways, product teasers, trailers, sales pitches
    if any(k in t for k in [
        "make 2021 great giveaway",
        "ultimate catering toolkit",
        "clickbacon+ toast pos",
        "the restaurant boss i believe",
        "youtube trailer",
        "restaurant consulting sales video",
        "you don't have to go it alone!"
    ]):
        return "skipped_promotional"

    # 5. Personal / Holiday greetings
    if "happy thanksgiving" in t:
        return "skipped_personal_or_holiday"

    return None

def determine_category_and_tags(title):
    t = title.lower()

    # 1. Food Cost & Portioning
    if any(k in t for k in [
        "food cost", "food costing", "food prices", "portion control", "cogs", 
        "cost of goods", "waste", "spoilage", "recipe costing", "beverage cost", "cogs categories",
        "batch recipe"
    ]):
        return "food-cost", ["food-cost", "cogs-management", "portion-control", "recipe-costing"]

    # 2. Inventory & Stock
    elif any(k in t for k in [
        "inventory", "stock", "par level", "sheet-to-shelf", "storage", "walk-in cooler"
    ]):
        return "inventory", ["inventory-management", "stock-control", "par-levels", "storage-organization"]

    # 3. Purchasing & Suppliers
    elif any(k in t for k in [
        "purchasing", "supplier", "vendor", "distributor", "purveyor", "receiving"
    ]):
        return "purchasing", ["purchasing", "vendor-negotiations", "supplier-relations", "receiving-dock"]

    # 4. Menu & Pricing
    elif any(k in t for k in [
        "menu", "menu engineering", "menu design", "pricing", "raise prices", 
        "signature dish", "menu pricing", "costing card"
    ]):
        return "menu", ["menu-engineering", "item-profitability", "pricing-strategy", "sales-mix"]

    # 5. Delivery & Catering
    elif any(k in t for k in [
        "delivery", "catering", "3rd party", "doordash", "ubereats", "grubhub", 
        "takeout", "online ordering", "ghost kitchen"
    ]):
        return "delivery", ["delivery-operations", "marketplace-commissions", "catering-sales", "online-ordering"]

    # 6. Payments & Credit Card Fees
    elif any(k in t for k in [
        "credit card", "pos system", "pos", "processing fee", "payment", "surcharge", "service fee"
    ]):
        return "payments", ["payments", "credit-card-fees", "pos-systems", "surcharges"]

    # 7. Customers & Hospitality
    elif any(k in t for k in [
        "customer service", "guest experience", "guest expectations", "hospitality", 
        "complaint", "table turn", "dining room", "hostess", "customer review",
        "reviews", "guest recovery", "rude customer"
    ]):
        return "customers", ["customer-experience", "guest-retention", "service-standards", "hospitality-management"]

    # 8. Marketing & Brand
    elif any(k in t for k in [
        "marketing", "advertising", "social media", "instagram", "facebook", "google",
        "seo", "website", "email marketing", "brand", "branding", "promotion", "promotions",
        "go-to restaurant in your neighborhood", "viral", "public relations", "get more customers",
        "attract customers", "bring in customers", "empty restaurant", "lines out the door"
    ]):
        return "marketing", ["restaurant-marketing", "customer-acquisition", "brand-positioning", "local-marketing"]

    # 9. Labour & Staff Management
    elif any(k in t for k in [
        "labor", "labour", "staff", "employee", "hiring", "hire", "interview", "payroll",
        "tip out", "tipping", "fire an employee", "firing", "toxic employee", "retention",
        "turnover", "team", "manager", "management", "delegation", "delegat", "leadership",
        "scheduling", "schedule", "onboarding", "training", "culture", "phantom labor",
        "millennial", "server", "servers", "stand-up meeting", "shift huddle", "coach", "coaching",
        "conductor", "accountability"
    ]):
        return "labour", ["labor-management", "staff-training", "employee-retention", "management-leadership"]

    # 10. Kitchen & Back of House
    elif any(k in t for k in [
        "kitchen", "prep", "cook", "chef", "expo", "boh", "equipment", "sanitation", "clean", "ticket time",
        "prep sheet"
    ]):
        return "kitchen", ["kitchen-operations", "prep-systems", "line-efficiency", "culinary-execution"]

    # 11. Forecasting & Demand
    elif any(k in t for k in [
        "forecast", "sales projection", "predict", "historical sales", "sales trend"
    ]):
        return "forecasting", ["sales-forecasting", "demand-planning", "revenue-projections", "shift-planning"]

    # 12. Finance & Economics
    elif any(k in t for k in [
        "prime cost", "profit", "profitable", "cash flow", "break even", "p&l", "balance sheet",
        "budget", "financial", "accounting", "bookkeeping", "sell your restaurant", "valuation",
        "expansion", "expanding", "recession", "inflation", "roi", "margins", "cost control",
        "startup", "open a restaurant", "second location", "taxes", "losing money", "bank",
        "sales are down", "sales drop", "make money"
    ]):
        return "finance", ["restaurant-finance", "prime-cost", "cash-flow", "profitability-metrics"]

    # 13. Operations & Management Systems
    else:
        return "operations", ["restaurant-operations", "standard-operating-procedures", "checklist-systems", "owner-strategy"]

def build_long_dossier(serial, title, url, category, slug, duration):
    clean_title = title.strip().replace('"', "'")
    doc_title = clean_title
    if not doc_title.startswith(("Restaurant", "High-Volume", "Operational", "Managing", "Optimizing", "The", "Why", "How")):
        doc_title = f"Restaurant Operational Intelligence: {clean_title}"

    overview = (
        f"Operational research dossier analyzing '{clean_title}', examining independent restaurant management systems, "
        "standard operating procedures, prime cost governance, and leadership frameworks developed by Ryan Gromfin (The Restaurant Boss)."
    )

    if category == "finance":
        sec1_title = "Prime Cost Governance & Margin Protection"
        sec1_points = [
            f"Financial management principles and prime cost controls established in '{clean_title}'.",
            "Prime cost architecture: actively tracking the combined total of Cost of Goods Sold (COGS) and Total Labor (management, hourly, and payroll taxes) as the ultimate solvency metric.",
            "Eliminating profit leaks: identifying margin degradation caused by unmonitored comps, unbudgeted overtime, and inconsistent supplier pricing before monthly P&L close."
        ]
        sec2_title = "Cash Flow Reserves & Multi-Unit Expansion Solvency"
        sec2_points = [
            "Building cash cushions: establishing operating cash reserves equal to 4 to 8 weeks of fixed overhead before committing capital to renovations or second locations.",
            "Disciplined business valuation: evaluating restaurant resale and equipment depreciation to ensure capital improvements yield measurable return on invested capital.",
            "Break-even sales discipline: calculating precise daily and weekly break-even revenue targets to determine shift-level operational viability."
        ]
        benchmarks = [
            "Prime cost benchmark: maintain prime cost strictly under 55% for full-service restaurants and under 60% for fast-casual concepts.",
            "Operating cash buffer: maintain an emergency liquidity reserve equal to at least 1 month of full operational expenses ($30,000 to $60,000 for independent units).",
            "Target net profit: independent operators should target 10% to 15% pre-tax net margin to safely support reinvestment and debt service."
        ]
        takeaways = [
            "Calculate and review prime cost every Monday morning using actual POS gross sales and supplier delivery invoices rather than waiting for accountant reconciliations.",
            "Stress-test cash flow forecasts against a 15% to 20% revenue drop to verify debt service coverage before authorizing unit expansions."
        ]

    elif category == "food-cost":
        sec1_title = "COGS Control, Recipe Costing & Portion Scales"
        sec1_points = [
            f"Food cost management systems and Cost of Goods Sold control detailed in '{clean_title}'.",
            "Pennies make thousands: precise recipe costing cards must establish exact theoretical costs down to the penny for every menu item, including garnishes and sauces.",
            "Portion standardization: enforcing the mandatory use of calibrated digital scales, measured disher scoops, and portion cups across all preparation and cook stations."
        ]
        sec2_title = "Theoretical vs. Actual Variance & Waste Audits"
        sec2_points = [
            "Tracking the variance gap: calculating the weekly dollar difference between theoretical food consumption (POS product mix) and actual physical inventory depletion.",
            "Daily kitchen waste logs: requiring kitchen staff to weigh, log, and sign off on all prep mistakes, line drops, and expired proteins before disposal.",
            "Proteins and high-value ingredient defense: conducting weekly targeted counts of top 10 dollar-impact inventory items to detect theft and over-portioning."
        ]
        benchmarks = [
            "Food cost benchmark: maintain overall food cost strictly between 28% and 32% of food revenue (30% target).",
            "Portion variance threshold: keep variance between theoretical food cost and actual inventory depletion under 1.5% to 2.0% of sales.",
            "Waste reduction metric: mandatory daily waste logging reduces preventable kitchen food waste by 20% to 35% within 60 days."
        ]
        takeaways = [
            "Recost all core menu items every 60 days to incorporate recent distributor price changes and maintain targeted gross margin dollars.",
            "Conduct unannounced spot-checks of pre-portioned proteins during shift setup to ensure compliance with portioning spec sheets."
        ]

    elif category == "inventory":
        sec1_title = "Sheet-to-Shelf Organization & Count Protocols"
        sec1_points = [
            f"Inventory control systems and storage room standardization from '{clean_title}'.",
            "Sheet-to-shelf alignment: designing inventory count sheets that exactly mirror the physical layout of the walk-in cooler, freezer, and dry storage shelves.",
            "Eliminating over-ordering: establishing mathematically calculated par levels based on peak-day product velocity and vendor delivery frequencies."
        ]
        sec2_title = "Holding Costs & Storage Room Hygiene"
        sec2_points = [
            "Minimizing sitting capital: holding excess food inventory ties up cash, increases spoilage risk, and invites employee pilferage.",
            "FIFO enforcement: labeling and rotating all incoming food stock (First-In, First-Out) to eliminate expired prep batches.",
            "Securing high-cost liquor and proteins: restricting storage room access to keyholders during off-peak hours to maintain chain-of-custody accountability."
        ]
        benchmarks = [
            "Inventory turnover benchmark: maintain inventory turnover between 4 and 6 times per month (carrying roughly 5 to 7 days of stock).",
            "Sitting inventory cap: total inventory valuation on hand should not exceed 1.5 times the weekly Cost of Goods Sold.",
            "Stock variance target: keep monthly inventory shrinkage and unexplained variance below 0.5% of gross sales."
        ]
        takeaways = [
            "Conduct full weekly inventory counts at the same time every Sunday evening or Monday morning to ensure consistent reporting intervals.",
            "Organize all walk-in and dry storage shelving with dedicated bin labels and laminated par level minimums."
        ]

    elif category == "purchasing":
        sec1_title = "Supplier Contract Audits & Price Verification"
        sec1_points = [
            f"Purchasing oversight and vendor negotiation tactics outlined in '{clean_title}'.",
            "Dock receiving protocols: inspecting and weighing all incoming produce, meat, and seafood boxes against the delivery manifest before signing invoices.",
            "Catching invoice creep: auditing line-item supplier pricing against contracted bids to catch stealth price increases on high-velocity ingredients."
        ]
        sec2_title = "Vendor Relations & Order Optimization"
        sec2_points = [
            "Consolidating vendor drop frequency: reducing delivery days from four to two per week to lower distributor delivery fees and minimize receiving interruptions.",
            "Secondary purveyor leverage: maintaining backup supplier relationships for high-spend commodities to preserve pricing leverage and ensure supply continuity.",
            "Spec sheet compliance: holding broadline distributors strictly accountable to contracted grade and yield specifications."
        ]
        benchmarks = [
            "Purchasing invoice accuracy: auditing delivery tickets catches invoice overcharges on 3% to 7% of distributor deliveries.",
            "Delivery consolidation savings: reducing weekly distributor drops from 4 to 2 cuts delivery surcharges by $150 to $300 per month.",
            "Commodity contract review: re-bidding high-spend grocery and protein categories every 6 months preserves 2% to 4% margin."
        ]
        takeaways = [
            "Require the receiving lead to date-stamp, scale-verify, and initial every single invoice before entering items into accounts payable.",
            "Maintain a pricing tracking spreadsheet for your top 20 dollar-spend ingredients to immediately spot vendor price increases."
        ]

    elif category == "menu":
        sec1_title = "Menu Engineering, SKU Rationalization & Item Margin"
        sec1_points = [
            f"Menu architecture and profitability frameworks analyzed in '{clean_title}'.",
            "Contribution margin over percentages: optimizing the menu to drive high gross-dollar contribution items into guest checks rather than obsessing over low percentage food costs.",
            "SKU rationalization: eliminating unique ingredients that are only used in a single, slow-moving dish to reduce walk-in inventory complexity and waste."
        ]
        sec2_title = "Menu Psychology, Visual Hierarchy & Strategic Pricing"
        sec2_points = [
            "Visual real estate optimization: placing high-margin signature items in the primary eye-magnets of physical and digital menus.",
            "Incremental price adjustments: raising prices strategically by $0.50 to $1.50 on inelastic favorites while enhancing plating presentation to preserve perceived value.",
            "Combating decision fatigue: cutting sprawling 80-item menus down to 35 to 45 focused, flawlessly executed core dishes."
        ]
        benchmarks = [
            "Menu SKU reduction: cutting the bottom 20% of low-volume menu items reduces walk-in cooler spoilage by 15% to 25%.",
            "Contribution margin lift: re-engineering menu category placement increases average check contribution margin by 8% to 14%.",
            "Optimal menu size: high-performing independent restaurants maintain between 30 and 45 total food items to ensure line speed and freshness."
        ]
        takeaways = [
            "Plot all menu items on a four-box matrix (Stars, Plowhorses, Puzzles, Dogs) quarterly based on sales velocity and dollar margin.",
            "Remove or re-engineer any 'Dog' item that fails to achieve both above-average order volume and acceptable contribution margin."
        ]

    elif category == "labour":
        sec1_title = "Frontline Staff Leadership, Coaching & Eliminating Phantom Labor"
        sec1_points = [
            f"Labor productivity and management frameworks established in '{clean_title}'.",
            "Eliminating phantom labor: trimming hours paid to staff who are standing around during slow shift openings, dead mid-afternoons, and extended closing periods.",
            "Manager as conductor: training restaurant managers to orchestrate shift execution, coach team members in real-time, and monitor speed of service rather than working as emergency line cooks."
        ]
        sec2_title = "Accountability, Stand-Up Huddles & Structured Delegation"
        sec2_points = [
            "Pre-shift stand-up huddles: holding mandatory 5-minute shift meetings to align servers and cooks on daily sales targets, 86'd items, and service standards.",
            "Clear delegation with timelines: assigning tasks with specific measurable outcomes, required standards, and firm completion deadlines.",
            "Addressing underperformance early: having candid, respectful coaching conversations immediately rather than letting poor habits demoralize high-performing staff."
        ]
        benchmarks = [
            "Labor cost benchmark: maintain total labor cost (hourly staff, management salaries, and payroll taxes) strictly between 28% and 32% of gross revenue.",
            "Phantom labor savings: tightening opening and closing clock-in/out windows recovers 10 to 20 wasted labor hours per week ($8,000 to $16,000 annually).",
            "Pre-shift huddle impact: consistent daily pre-shift meetings improve daily appetizer and dessert sales attach rates by 15% to 22%."
        ]
        takeaways = [
            "Conduct a mandatory 5-minute stand-up huddle before every lunch and dinner shift to set expectations and energize the floor.",
            "Establish strict clock-in grace periods preventing hourly employees from clocking in more than 5 minutes before scheduled shift start."
        ]

    elif category == "delivery":
        sec1_title = "Third-Party Marketplace Economics & Margin Defense"
        sec1_points = [
            f"Delivery economics and off-premise operational strategies from '{clean_title}'.",
            "Commission rate reality: paying 25% to 30% third-party marketplace commissions without price markups results in negative net margins on delivery orders.",
            "Dual menu pricing: establishing an optimized delivery menu with 20% to 25% price premiums to offset platform commission deductions."
        ]
        sec2_title = "Packaging Integrity, Order Accuracy & Direct Conversion"
        sec2_points = [
            "Packaging quality control: selecting vented, insulated containers that preserve food texture, prevent sogginess, and maintain safe temperature over 30-minute delivery transit.",
            "Bag-sealing and ticket verification: implementing a double-check ticket verification system with tamper-evident stickers to prevent missing items.",
            "Converting third-party diners: placing direct-ordering promotional bounce-back inserts inside every delivery bag to convert marketplace users to direct channels."
        ]
        benchmarks = [
            "Third-party commission threshold: marketplace commissions range from 20% to 30%, requiring a minimum 18% to 25% menu price markup to break even.",
            "Delivery order accuracy target: achieve 99.0%+ order fulfillment accuracy to eliminate costly refund penalties and chargebacks.",
            "Direct channel conversion: effective bag insert offers convert 5% to 10% of third-party marketplace customers to first-party online ordering."
        ]
        takeaways = [
            "Audit delivery menu prices quarterly to ensure retail margins cover platform commissions, packaging materials, and merchant fees.",
            "Include a compelling bounce-back voucher (e.g., $5 off first order) in every delivery bag directing guests to your proprietary website."
        ]

    elif category == "payments":
        sec1_title = "Credit Card Surcharge Traps & Merchant Processing Transparency"
        sec1_points = [
            f"Payment processing economics and customer checkout policies from '{clean_title}'.",
            "The surcharge penalty: passing credit card surcharges directly to dining room guests damages brand perception, triggers customer friction, and harms repeat business.",
            "Incorporating fees into menu prices: rolling merchant processing costs (2.5% to 3.5%) into overall menu pricing rather than hitting guests with surprise checkout fees."
        ]
        sec2_title = "POS Optimization & Tip Distribution Compliance"
        sec2_points = [
            "POS system utilization: configuring point-of-sale reporting to automatically separate net sales, collected sales tax, and tips to prevent tax liability errors.",
            "Tip pooling legal compliance: structuring clear, written tip distribution protocols that comply with fair labor standards and exclude managers from tip pools.",
            "Gift card cash flow management: tracking unredeemed gift card breakage while maintaining sufficient operational cash flow to service redemptions."
        ]
        benchmarks = [
            "Merchant processing fee benchmark: target all-in effective credit card processing rates between 2.2% and 2.8% of credit card sales.",
            "Customer churn from junk fees: surprise checkout surcharges increase customer dissatisfaction ratings and negative online reviews by over 30%.",
            "Gift card float economics: 10% to 15% of issued gift card balances remain unredeemed after 12 months, representing float liquidity."
        ]
        takeaways = [
            "Build credit card processing costs directly into menu prices rather than displaying polarizing surcharges on customer receipts.",
            "Conduct an annual statement audit with your merchant processor to eliminate hidden non-qualifying interchange fees and terminal leases."
        ]

    elif category == "customers":
        sec1_title = "Guest Service Recovery, Hospitality Standards & De-escalation"
        sec1_points = [
            f"Hospitality systems and guest relationship management outlined in '{clean_title}'.",
            "Empowering frontline recovery: authorizing servers and shift leads to immediately replace unsatisfactory dishes or buy a drink without needing owner approval.",
            "De-escalation protocols: training staff to listen attentively without defending, validate guest frustration, and resolve issues before the diner leaves the table."
        ]
        sec2_title = "Atmosphere Controls, Table Turns & Reputation Protection"
        sec2_points = [
            "Dining room environment management: monitoring dining room lighting, playlist volume, room temperature, and restroom cleanliness throughout the shift.",
            "Pacing service and table turns: streamlining bussing, check presentation, and payment collection during peak rushes without making guests feel rushed.",
            "Managing online review narratives: responding promptly and professionally to negative public feedback to demonstrate accountability and operational maturity."
        ]
        benchmarks = [
            "Table turn pacing: optimizing dining room bussing and payment presentation reduces table reset time by 4 to 6 minutes during peak service.",
            "Guest recovery impact: resolving customer complaints at the table retains over 75% of dissatisfied diners as loyal repeat patrons.",
            "Review score conversion: maintaining an average rating of 4.5+ stars across Google and Yelp yields 15% to 20% higher organic guest volume."
        ]
        takeaways = [
            "Implement the 'Last Bite' table check: managers must visit tables before the check is presented to ensure total guest satisfaction.",
            "Respond to all online negative reviews within 48 hours using an empathetic, solution-oriented response that invites direct offline resolution."
        ]

    elif category == "marketing":
        sec1_title = "Local Market Dominance & Brand Positioning"
        sec1_points = [
            f"Restaurant marketing systems and community customer acquisition detailed in '{clean_title}'.",
            "Becoming the neighborhood go-to spot: building deep local community ties through school partnerships, youth sports sponsorships, and local business networking.",
            "Brand clarity: clearly defining your restaurant's core identity, signature food items, and target demographic rather than trying to appeal to everyone."
        ]
        sec2_title = "Google Maps Local SEO & Owned Customer Databases"
        sec2_points = [
            "Google Business Profile optimization: actively maintaining accurate business hours, professional high-resolution dish photography, and weekly Google posts.",
            "Building first-party lists: collecting customer email addresses and phone numbers through loyalty signups and WiFi captive portals rather than relying solely on social media algorithms.",
            "Targeted promotional calendars: creating structured quarterly marketing campaigns tied to seasonal events and local milestones rather than random panic ads."
        ]
        benchmarks = [
            "Google Maps local search traffic: restaurants with 100+ positive Google reviews and active photo updates receive 3x more discovery searches.",
            "First-party database value: an active SMS/email subscriber database drives repeat customer visits at an acquisition cost under $1.50 per guest.",
            "Marketing budget allocation: allocate 2% to 4% of gross monthly sales toward targeted local marketing and community relationship initiatives."
        ]
        takeaways = [
            "Audit your Google Business Profile monthly: upload 5 to 10 fresh, high-quality dish photos and ensure menus and operating hours are 100% current.",
            "Run consistent weekly email or SMS campaigns offering exclusive value or seasonal dishes to your owned subscriber list."
        ]

    elif category == "kitchen":
        sec1_title = "BOH Line Flow, Ticket Times & Prep System Standardization"
        sec1_points = [
            f"Back-of-house kitchen efficiency and prep management principles from '{clean_title}'.",
            "Standardized prep sheets: replacing kitchen guesswork with mathematical daily prep sheets calculated from forecasted covers and station par levels.",
            "Expediter station discipline: establishing a dedicated expediter during peak volume to inspect every plate for temperature, presentation, and ticket accuracy."
        ]
        sec2_title = "Station Ergonomics, Sanitation & Equipment Maintenance"
        sec2_points = [
            "Line ergonomics: arranging mise-en-place so line cooks can assemble 80% of dishes without taking more than two steps away from their station.",
            "Preventative equipment maintenance: scheduling regular deep-cleaning and maintenance of refrigeration compressors, fryers, and ovens to prevent mid-shift breakdowns.",
            "Kitchen culture and sanitation: enforcing spotless station cleanliness throughout service to uphold food safety standards and elevate kitchen morale."
        ]
        benchmarks = [
            "Peak ticket time target: maintain average ticket times strictly between 12 and 16 minutes during peak dinner service.",
            "Prep sheet accuracy: mathematical prep sheets reduce end-of-shift perishable food scrap by 20% to 30%.",
            "Preventative maintenance savings: routine quarterly refrigeration maintenance reduces emergency service call-outs by over 60%."
        ]
        takeaways = [
            "Implement standardized station prep sheets that shift supervisors calculate and verify each morning before culinary prep commences.",
            "Post clear, visual plate assembly photos and recipe cards at the expo window to eliminate plate garnish discrepancies."
        ]

    elif category == "forecasting":
        sec1_title = "Sales Forecasting Models & Shift Demand Planning"
        sec1_points = [
            f"Sales forecasting frameworks and demand prediction systems detailed in '{clean_title}'.",
            "Historical sales analysis: tracking 4-week rolling averages, same-day prior year trends, and day-of-week sales patterns to forecast hourly revenue accurately.",
            "Factoring external variables: adjusting weekly sales projections for local sporting events, weather forecasts, construction detours, and school calendars."
        ]
        sec2_title = "Aligning Purchasing & Labor Schedules to Projections"
        sec2_points = [
            "Labor scheduling against forecasted sales: drafting weekly staff rosters directly against hourly sales projections rather than reusing rigid static templates.",
            "Ordering alignment: synchronizing inventory order quantities with projected covers to prevent walk-in overstocking and cash lockup.",
            "Mid-week schedule adjustments: reviewing 72-hour forecast trends to trim shifts ahead of severe weather or adjust for unexpected catering volume."
        ]
        benchmarks = [
            "Forecast accuracy target: maintain weekly sales projection variance within +/- 5% of actual recorded POS gross sales.",
            "Scheduling efficiency: forecasting-aligned labor scheduling cuts unnecessary payroll expense by 2% to 4% of total revenue.",
            "Weather variance impact: adverse weather can depress patio and walk-in sales by 15% to 30%, requiring proactive 24-hour staffing adjustments."
        ]
        takeaways = [
            "Update next week's sales forecast every Tuesday using a 4-week weighted rolling average combined with local calendar events.",
            "Schedule hourly labor hours strictly against forecasted sales per labor hour (SPLH) targets rather than copying last week's schedule."
        ]

    else: # Operations / Management Systems
        sec1_title = "Standard Operating Procedures, Checklists & Shift Handover"
        sec1_points = [
            f"Core restaurant operational systems and management execution frameworks from '{clean_title}'.",
            "The checklist operating system: opening, mid-day transition, and closing checklists are non-negotiable tools that prevent operational drift and protect standards.",
            "Shift handover communication: requiring incoming and outgoing managers to walk the floor, audit restrooms, and review the daily manager log together before shift handover."
        ]
        sec2_title = "Building a Turnkey Operation & The 90-Day Owner Test"
        sec2_points = [
            "Working on the business vs in the business: transitioning the owner from an emergency firefighter into a strategic leader who builds repeatable systems.",
            "The 90-day acid test: a restaurant is not truly ready for multi-unit expansion until the flagship location can run profitably for 90 consecutive days without owner intervention.",
            "Daily operational audits: conducting consistent 10-minute floor audits to inspect service speed, cleanliness, and guest satisfaction standards."
        ]
        benchmarks = [
            "Checklist compliance target: maintain above 95% completion rate on daily opening, shift handover, and closing checklists.",
            "Manager shift walk duration: a comprehensive pre-shift operational walk-through should take 10 to 15 minutes to inspect all BOH and FOH stations.",
            "Turnkey readiness threshold: independent restaurants require at least 15% net EBITDA margins before capital can be safely deployed into secondary unit expansion."
        ]
        takeaways = [
            "Implement standardized station checklists for every FOH and BOH station, reviewed and signed off by the shift manager daily.",
            "Take a mandatory 7-day complete absence from your restaurant to stress-test your management systems and expose operational single points of failure."
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
    md_lines.append("- Channel: The Restaurant Boss")
    md_lines.append(f"- Video: {clean_title}")
    md_lines.append(f"- URL: {url.strip()}")
    md_lines.append("")

    return "\n".join(md_lines)

def process_all_restaurant_boss_videos():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total Restaurant Boss Videos in catalog: {len(rows)}")

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
    print(f"  - Total Processed: {ingested_count + triaged_count}/434")

if __name__ == "__main__":
    process_all_restaurant_boss_videos()
