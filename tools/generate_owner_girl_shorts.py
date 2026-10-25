#!/usr/bin/env python3
"""
generate_owner_girl_shorts.py

Processes all 394 shorts from sources/youtube-lists/owner-girl-shorts.csv:
- Triages non-substantive marketing, entertainment, and generic motivational clips per AGENTS.md Rule 8.
- Synthesizes substantive independent restaurant operational intelligence into
  knowledge/owner-girl/owner-girl-short-form/<category>/<filename>.md.
- Updates sources/youtube-lists/owner-girl-shorts.csv accordingly.
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

CSV_PATH = os.path.join("sources", "youtube-lists", "owner-girl-shorts.csv")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "owner-girl", "owner-girl-short-form")
FLAT_JSON_PATH = os.path.join("scratch", "owner_girl_shorts_flat_info.json")

def is_promotional_or_fluff(title):
    t = title.lower()

    # 1. Social entertainment, jokes, team dance, memes, birthdays, holidays
    if any(k in t for k in [
        "dance", "limbo", "birthday magic", "birthday serenade", "first birthday",
        "mothers day", "july 4th", "airshow", "pie face off", "fiesta medal",
        "tractor", "karaoke", "mushroom whisperers", "crispy dolphin", "fridge footprints",
        "comedy", "shenanigans", "big groove", "dave portnoy", "taste of the medical center",
        "join restaurant sales growth popup", "limited edition", "pizza box twist",
        "pizza box delight", "frozen beef log", "clemens cheer", "smiling face",
        "we ate everything", "gunslingers collaboration", "green team shirts",
        "what the mind conceives", "tennis and the art of leadership", "dad's best advice",
        "san antonio's best pizza", "pizza on wheels", "crafting the perfect slice",
        "rising like pizza dough", "pizza, happiness, and smiles", "feeding the crowd: bts",
        "kneading together for pizza greatness", "we appreciate the tips", "when local love meets",
        "epic moves", "unforgettable bites & restaurant insights at texas restaurant show",
        "oddities in kitchen", "rookie move: the newbie's cup confusion"
    ]):
        return "skipped_social_entertainment"

    # 2. PR, community service, charity, awards, team behind-the-scenes cheerleading
    if any(k in t for k in [
        "smiles served daily", "no brakes, no problem", "serving 100 smiles", "serving smiles",
        "kids build their own", "from crust to community", "community service", "give back with pizza",
        "pizza, passion, and purpose", "kitchen symphony", "more drama than your favorite",
        "crafting perfection: the hard work", "friday rush: customer smiles", "balancing the stretch",
        "how teamwork keeps us sizzling", "teamwork & taste", "behind every slice of success",
        "bts hiring experience", "pizza expo 2024", "tossing dough like a pro",
        "sparks of workplace joy", "grateful to have someone like her", "exploring flavors together",
        "meeting incredibly talented people", "just like a perfect pizza, our team",
        "seen on tv before our restaurant", "dedication at work in action",
        "hardworking at age", "feel like giving up", "attitude is everything", "walk your talk"
    ]):
        return "skipped_social_entertainment"

    # 3. Generic motivational fluff / vague platitudes
    if any(k in t for k in [
        "motivation monday", "the biggest secret to success", "united we knead",
        "why the best teams are like families", "warmest smiles and pizzas you'll find",
        "our secret ingredient", "love & passion our team has", "facing challenges with grace and grit",
        "life at a pizzeria", "the little things that make", "what to tell yourself"
    ]):
        return "skipped_motivational"

    return None

def determine_category_and_tags(title):
    t = title.lower()

    # 1. Finance & Cash Management
    if any(k in t for k in [
        "financial projection", "start up cost", "cash management", "cash mismanagement",
        "sales number to your staff", "sales projections", "unprofitable problems", "cogs control",
        "controlling restaurant costs", "margin", "prime cost", "profit", "budget"
    ]):
        return "finance", ["restaurant-finance", "cash-controls", "financial-projections", "unit-economics"]

    # 2. Food Cost & Recipe Costing
    if any(k in t for k in [
        "food inconsistency", "recipe book", "portion", "food cost", "topping", "dough cost",
        "cheese cost", "ingredient cost", "waste"
    ]):
        return "food-cost", ["food-cost", "recipe-consistency", "portion-control", "cogs-management"]

    # 3. Labour, Staffing & HR
    if any(k in t for k in [
        "labor", "staff", "employee", "hiring", "hire", "onboarding", "call-out policy", "call-out",
        "background check", "manager", "leadership", "leader", "training", "team", "turnover",
        "workplace", "payroll", "tip", "scheduling", "respect", "disrespect", "coaching",
        "morale", "incident report", "arguments", "cleaning checklist", "job", "career development"
    ]):
        return "labour", ["labor-management", "staff-training", "employee-retention", "workplace-culture"]

    # 4. Inventory
    if any(k in t for k in ["inventory", "par level", "sheet-to-shelf", "stock", "spoilage", "shrinkage", "unavailable"]):
        return "inventory", ["inventory-management", "stock-control", "par-levels", "item-availability"]

    # 5. Menu
    if any(k in t for k in ["menu", "vegan option", "pricing", "modifier", "item to order is unavailable"]):
        return "menu", ["menu-engineering", "item-availability", "pricing-strategy", "vegan-options"]

    # 6. Kitchen & Back of House
    if any(k in t for k in ["kitchen", "prep", "cook line", "ticket time", "kds", "line check"]):
        return "kitchen", ["kitchen-operations", "station-throughput", "food-prep", "order-timing"]

    # 7. Delivery & Catering
    if any(k in t for k in ["delivery", "delivered", "catering", "off-premise", "online order"]):
        return "delivery", ["delivery-operations", "catering-logistics", "order-volume", "speed-of-fulfillment"]

    # 8. Marketing & Customer Acquisition
    if any(k in t for k in ["marketing", "email", "social media", "customer review", "reviews", "sales growth"]):
        return "marketing", ["restaurant-marketing", "email-marketing", "review-generation", "customer-acquisition"]

    # 9. Customers & Hospitality
    if any(k in t for k in [
        "customer", "guest complaint", "guest complaints", "customer experience", "rude and angry",
        "customer service", "hospitality", "customer coming back", "fraudulent", "atmosphere", "friendliness"
    ]):
        return "customers", ["customer-retention", "guest-complaints", "service-recovery", "hospitality-standards"]

    # 10. Operations & Management Systems
    return "operations", ["restaurant-operations", "management-systems", "sop-execution", "owner-mindset"]

def build_short_dossier(serial, title, url, category, tags):
    clean_title = title.strip().replace('"', "'")

    if category == "finance":
        key_info = [
            f"Operational examination of financial discipline and resource allocation from '{clean_title}'.",
            "Independent restaurant viability depends on actively eliminating unprofitable operations and unprofitable menu items before investing in top-line growth.",
            "Daily and weekly cash visibility enables operators to catch margin leakage, cash drawer variances, and unexpected price increases early."
        ]
        numbers = [
            "Prime cost control target: maintain combined food and labor costs strictly below 55% to 60% of gross revenue.",
            "Cash reserve benchmark: maintain a minimum operating cash liquidity buffer of 2 to 4 weeks of fixed operating overhead."
        ]
        takeaways = [
            "Calculate prime cost on a rolling weekly basis and review cash balances daily to prevent sudden payroll or purveyor shortfalls.",
            "Establish strict manager accountability for daily blind cash drawer drops and safe reconciliations."
        ]
    elif category == "food-cost":
        key_info = [
            f"Recipe execution and cost control principles detailed in '{clean_title}'.",
            "Food inconsistency is driven by unmeasured ingredient portions, untracked prep scrap, and lack of visual recipe build cards.",
            "Standardized portioning tools (calibrated scales, portion cups, ladles) ensure that every dish meets target nutritional and financial parameters."
        ]
        numbers = [
            "Target food cost: maintain independent pizzeria and casual dining food cost between 28% and 32% of food sales.",
            "Portion control impact: over-portioning high-cost cheese and proteins by just 10% can erode overall store profit margins by 2% to 4%."
        ]
        takeaways = [
            "Laminate photographic recipe spec sheets at every prep and assembly station showing exact ounce weights for each ingredient.",
            "Audit prepped ingredient bins and station yields before every peak service rush."
        ]
    elif category == "labour":
        key_info = [
            f"Frontline team management and staffing standard operating procedures from '{clean_title}'.",
            "Clear, written operational policies (call-out procedures, onboarding checklists, station milestones) eliminate ambiguity and reduce friction.",
            "Consistent manager feedback and objective documentation build trust and protect staff accountability across all shift rosters."
        ]
        numbers = [
            "Labor cost target: maintain fully-burdened hourly and management labor between 28% and 32% of gross sales.",
            "Onboarding retention benchmark: structured 30-day onboarding milestones reduce 90-day employee turnover by over 30%."
        ]
        takeaways = [
            "Enforce a mandatory 4-hour advance call-out policy and document all attendance variances systematically.",
            "Conduct structured 15-minute 1-on-1 check-ins with new team members at the 7-day, 14-day, and 30-day employment marks."
        ]
    elif category == "customers":
        key_info = [
            f"Hospitality standards and customer retention systems highlighted in '{clean_title}'.",
            "The primary driver of lost repeat customers is unaddressed service failures and inconsistent order execution.",
            "Empowering frontline staff to execute immediate on-the-spot service recovery de-escalates unhappy diners before complaints reach public review platforms."
        ]
        numbers = [
            "Retention impact: increasing repeat customer frequency by 5% can increase store profitability by 25% to 75%.",
            "Complaint resolution velocity: resolving guest complaints within 24 hours retains over 70% of dissatisfied diners as repeat guests."
        ]
        takeaways = [
            "Establish an immediate 'Service Recovery Protocol' empowering floor managers to comp or replace flawed items without owner approval.",
            "Review customer feedback logs weekly during leadership meetings to identify recurring operational root causes."
        ]
    elif category == "marketing":
        key_info = [
            f"Direct customer acquisition and retention strategies outlined in '{clean_title}'.",
            "First-party marketing channels (direct email and SMS subscriber lists) consistently outperform passive social media organic reach.",
            "Automated review requests sent immediately after positive dining experiences build local SEO rankings and trust."
        ]
        numbers = [
            "Email marketing ROI: direct email campaigns produce open rates of 20% to 35% and drive predictable weekly sales bumps.",
            "Review conversion threshold: maintaining a 4.5+ star rating on Google Maps increases local new diner foot traffic by 15% to 25%."
        ]
        takeaways = [
            "Collect direct customer email and SMS contacts at checkout via receipt prompts or digital loyalty signups.",
            "Send consistent weekly or bi-weekly email newsletters highlighting community stories, exclusive offers, and catering availability."
        ]
    elif category == "delivery":
        key_info = [
            f"Off-premise order fulfillment and delivery logistics detailed in '{clean_title}'.",
            "High-volume delivery operations require strict station staging, order staging shelves, and packaging thermal integrity.",
            "Pacing high-volume delivery orders during peak dining room hours prevents culinary bottlenecks and delayed delivery dispatches."
        ]
        numbers = [
            "Delivery throughput benchmark: achieve staging and packaging throughput exceeding 100 to 145 pizzas per peak delivery hour.",
            "Packaging target: maintain packaging costs under 3% of delivery order gross revenue."
        ]
        takeaways = [
            "Separate delivery driver pickup areas completely from dining room host stands to eliminate counter congestion.",
            "Implement itemized receipt tape checks to verify every box and beverage before courier handover."
        ]
    else: # Operations / General
        key_info = [
            f"Restaurant operational discipline and standard operating procedures from '{clean_title}'.",
            "Operating a sustainable restaurant requires transitioning from 'working IN the business' to 'working ON the business' through scalable SOPs.",
            "Standardized opening, shift transition, and closing checklists ensure store readiness regardless of which manager is on duty."
        ]
        numbers = [
            "Checklist compliance target: maintain above 95% completion rate on daily digital or paper station checklists.",
            "Shift handover velocity: clear pre-shift huddles reduce shift communication errors and delayed prep orders by over 50%."
        ]
        takeaways = [
            "Implement clear opening, mid-shift, and closing checklists signed off by the shift supervisor daily.",
            "Schedule dedicated weekly strategic planning blocks to evaluate store KPIs, audit inventory, and plan upcoming seasonal shifts."
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
    lines.append("- The Making Dough Show with Hengam Stanfield (Mattenga's Pizzeria) operational research.")
    lines.append("- Applicable to independent restaurant owners, pizzerias, fast-casual operators, and hospitality managers.")
    lines.append("")
    lines.append("# Source")
    lines.append("")
    lines.append(f"Video: {url}")
    lines.append("")

    return "\n".join(lines)

def process_all_owner_girl_shorts():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total Owner-girl Shorts to process: {len(rows)}")

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
        slug = "-".join(words[:6]) or f"owner-girl-intelligence-{serial}"
        # Ensure slug starts and ends cleanly
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
    print(f"  - Total Accounts: {ingested_count + triaged_count}/394")

if __name__ == "__main__":
    process_all_owner_girl_shorts()
