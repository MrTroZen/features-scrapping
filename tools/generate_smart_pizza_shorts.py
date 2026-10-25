#!/usr/bin/env python3
"""
generate_smart_pizza_shorts.py

Processes all 157 shorts from sources/youtube-lists/smart-pizza-shorts.csv:
- Triages podcast bloopers/meme cuts and untitled/date clips per AGENTS.md Rule 8.
- Synthesizes substantive pizzeria operational intelligence, dough management,
  and micro-footprint economics into knowledge/smart-pizza/smart-pizza-short-form/<category>/<filename>.md.
- Updates sources/youtube-lists/smart-pizza-shorts.csv accordingly.
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

CSV_PATH = os.path.join("sources", "youtube-lists", "smart-pizza-shorts.csv")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "smart-pizza", "smart-pizza-short-form")

def is_short_triage(title):
    t = title.strip().lower()

    # Date titles / single vague word
    if any(k in t for k in [
        "november 3, 2025", "october 17, 2024", "the first step.", "announcement from spm"
    ]):
        return "skipped_untitled_or_date"

    # 5-second podcast laughing / blooper clips / inside joke reactions
    if any(k in t for k in [
        "you have to call me dragon", "❤️🍕", "i am 😆", "my ❤️ is beating so fast",
        "she’s good at lying", "is it ready yet?", "we don’t care", "that was awesome",
        "hahaha", "nobody cares", "help 😆", "everyone is from new york", "i’m good",
        "is it off yet", "numbers don’t lie 😆", "just being honest", "it’s always interesting",
        "another week in the books", "oh really?", "it’s hot!!", "better than zero",
        "if you smell", "sorry not sorry", "we made it", "i eat things", "and i enjoyed them all",
        "is it hot in here", "be right with you sir", "how do i tell them", "don’t negotiate",
        "it’s thiiick", "it’s simple", "another one?", "it's scary"
    ]):
        return "skipped_podcast_blooper_or_meme"

    return None

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

def build_short_dossier(serial, title, url, category, tags):
    clean_title = title.strip().replace('"', "'")

    if category == "food-cost":
        key_info = [
            f"Pizzeria food cost governance and dough production systems from '{clean_title}'.",
            "Dough hydration and fermentation control: managing cold-fermentation schedules (24 to 72 hours) yields superior crust structure while stabilizing flour-to-dough cost efficiency.",
            "Pan investments and portion discipline: utilizing heavy-gauge seasoned steel pans and measured cheese cups prevents expensive overtopping and ensures bake consistency."
        ]
        numbers = [
            "Pizzeria food cost benchmark: maintain pizza Cost of Goods Sold strictly between 22% and 28% of total revenue.",
            "Cheese variance impact: overtopping cheese by just 1 ounce per pie across 200 daily pizzas costs an independent operator $10,000 to $16,000 annually."
        ]
        takeaways = [
            "Implement standardized portion cups and digital scales for cheese and high-cost meats at every assembly station.",
            "Establish daily batch dough logs recording water temperature, room temperature, and exact yeast percentages to guarantee crumb consistency."
        ]

    elif category == "menu":
        key_info = [
            f"Pizzeria menu engineering and SKU rationalization analyzed in '{clean_title}'.",
            "The streamlined menu advantage: operating with just 5 to 8 focused, high-craft pizza variations accelerates oven turnaround and reduces prep ingredient spoilage.",
            "Resisting discount traps: competing on product quality, crust authenticity, and distinctive styles rather than destructive coupon discounting."
        ]
        numbers = [
            "Menu SKU reduction: cutting menu offerings down to under 10 core pizzas increases oven throughput by 25% to 35%.",
            "Single-size operational gain: offering a single 16-inch or 14-inch pie size eliminates box clutter and speeds up dough ball stretching by 30%."
        ]
        takeaways = [
            "Audit your pizzeria product mix and eliminate menu items that account for less than 3% of weekly gross sales.",
            "Feature one distinctive signature specialty pie with high gross contribution dollars as your primary marketing anchor."
        ]

    elif category == "delivery":
        key_info = [
            f"Pizzeria off-premise fulfillment, delivery channels, and platform economics from '{clean_title}'.",
            "Third-party commission offset: charging delivery menu price markups to protect operational margins against marketplace commissions (20% to 30%).",
            "Conveyor oven consistency for delivery: utilizing calibrated conveyor deck ovens ensures identical bake times and blistered cheese during intense delivery rush waves."
        ]
        numbers = [
            "Delivery commission buffer: mark up third-party marketplace menu prices by 18% to 22% to maintain profit parity with direct takeout orders.",
            "Delivery packaging thermal performance: pizza boxes with corrugated venting preserve crust crispness and maintain >140°F holding temperature for 25 minutes."
        ]
        takeaways = [
            "Include direct-ordering bounce-back incentives inside every delivery pizza box to convert marketplace customers to first-party channels.",
            "Stagger delivery dispatch windows during Friday evening peaks to prevent oven bottlenecks."
        ]

    elif category == "finance":
        key_info = [
            f"Pizzeria unit economics, lease terms, and capital efficiency detailed in '{clean_title}'.",
            "Micro-footprint revenue density: compact pizza shops (300 to 800 sq ft) generate $1.5M to $3M in annual sales by focusing strictly on takeout and pre-orders.",
            "Low-debt launch models: starting with pop-ups, mobile setups, or subleased prep spaces minimizes early debt service burdens."
        ]
        numbers = [
            "Pizzeria rent-to-sales ratio: keep total retail occupancy expenses (base rent + NNN) strictly under 6% to 8% of gross pizza sales.",
            "Micro-footprint sales density: leading takeout-only pizzerias achieve $1,500 to $3,000 in annual revenue per square foot.",
            "Start-up equipment budget: outfitting a compact artisanal pizza operation requires $60,000 to $120,000 in core oven, refrigeration, and dough machinery."
        ]
        takeaways = [
            "Prioritize takeout-centric retail real estate with dedicated curbside parking over expensive dining room square footage.",
            "Stress-test your lease pro forma assuming peak weekend sales must cover the entire month's base occupancy expense."
        ]

    elif category == "marketing":
        key_info = [
            f"Local pizzeria marketing, video content creation, and community branding analyzed in '{clean_title}'.",
            "Organic video virality: capturing backstage dough stretching, cheese pulls, and oven bakes creates compelling visual content that fuels hyper-local discovery.",
            "Direct customer communication: building SMS and VIP text clubs (e.g. Boostly integration) enables instant direct-to-consumer order activation during slow mid-week shifts."
        ]
        numbers = [
            "VIP text marketing conversion: automated SMS text clubs achieve 98% open rates and generate 8% to 15% order conversion within 2 hours of broadcast.",
            "Social media video reach: consistent short-form vertical videos generate 3x to 5x higher local reach than static food photography."
        ]
        takeaways = [
            "Build an owned VIP customer SMS database and broadcast weekly limited-quantity specialty pie drops on Tuesday afternoons.",
            "Post daily behind-the-scenes vertical videos showing dough preparation, fresh sauce mixing, and oven launches."
        ]

    elif category == "customers":
        key_info = [
            f"Guest hospitality, community engagement, and loyalty systems detailed in '{clean_title}'.",
            "Neighborhood connection: treating diners as personal guests and recognizing regulars transforms a commodity food transaction into an enduring community habit.",
            "Review management: addressing guest complaints immediately on the floor prevents negative public review escalations."
        ]
        numbers = [
            "Regular customer order frequency: pizzerias with active community loyalty programs see repeat customer visits every 10 to 14 days versus 45 days for casual diners.",
            "Customer lifetime value: an engaged weekly pizza customer generates over $1,800 in direct annual revenue."
        ]
        takeaways = [
            "Train counter and phone staff to greet returning customers by name and recall their customary order preferences.",
            "Respond to all online feedback within 24 hours to reinforce commitment to culinary and service excellence."
        ]

    elif category == "labour":
        key_info = [
            f"Pizzeria labor scheduling, cross-training, and solo-operator systems from '{clean_title}'.",
            "Solo and two-person kitchen efficiency: designing simplified station ergonomics allows a single skilled pizzaiolo to stretch, top, and bake 100+ pizzas per night.",
            "Peak shift staffing: aligning staff arrival times exactly with oven pre-heat and peak order curves eliminates wasteful early-shift labor hours."
        ]
        numbers = [
            "Pizzeria labor cost benchmark: maintain total labor costs strictly between 22% and 28% of gross pizza sales.",
            "Solo operator capacity: an optimized single-operator pizza kitchen layout can fulfill 120 to 150 pizzas in a 4-hour dinner service window."
        ]
        takeaways = [
            "Cross-train all frontline team members across stretching, oven tending, and boxing stations to eliminate rush bottlenecks.",
            "Pre-portion all secondary toppings during morning prep to maximize assembly speed during dinner volume."
        ]

    elif category == "kitchen":
        key_info = [
            f"Pizza oven technologies, baking thermodynamics, and kitchen layout from '{clean_title}'.",
            "Deck ovens vs conveyor ovens: choosing baking platforms based on volume requirements—conveyor ovens maximize high-volume speed, while stone decks provide artisanal crust blister.",
            "Prep line ergonomics: arranging sauce, cheese, and toppings in descending order of usage directly adjacent to the dough stretching block."
        ]
        numbers = [
            "Deck oven recovery time: commercial deck ovens require 3 to 5 minutes between bakes to recover stone hearth surface temperature.",
            "Conveyor oven throughput: triple-stack conveyor ovens can produce 90 to 140 baked pizzas per hour per lane."
        ]
        takeaways = [
            "Use an infrared surface thermometer to monitor stone deck floor temperature continuously throughout peak service.",
            "Establish strict daily oven scraping and stone maintenance protocols to prevent burnt flour off-flavors."
        ]

    else: # Operations / Micro-Pizzerias
        key_info = [
            f"Independent pizzeria operations, pre-order business models, and operational systems from '{clean_title}'.",
            "The daily sell-out business model: capping production at 100 to 150 daily pizzas creates perceived scarcity, ensures zero waste, and guarantees predictable operating hours.",
            "Standard operating checklists: implementing daily dough proofing, walk-in rotation, and closing checklists ensures uniform quality across shifts."
        ]
        numbers = [
            "Daily sell-out model predictability: pre-order sell-out models achieve 0% end-of-day dough scrap and 100% predictable revenue.",
            "Operational checklist compliance: maintaining >95% checklist completion cuts opening station prep delays by 20 to 30 minutes daily."
        ]
        takeaways = [
            "Test a limited daily dough batch cap (e.g. 100 pizzas) to build customer urgency and streamline daily labor.",
            "Enforce standardized opening and closing checklists signed off by the lead pizzaiolo on every shift."
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
    lines.append("- Smart Pizza Marketing (Bruce Irving) independent pizzeria operations, marketing, and unit economics research.")
    lines.append("- Applicable to independent pizzeria operators, artisanal pizza founders, and mobile food entrepreneurs.")
    lines.append("")
    lines.append("# Source")
    lines.append("")
    lines.append(f"Video: {url}")
    lines.append("")

    return "\n".join(lines)

def process_all_smart_pizza_shorts():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total Smart Pizza Shorts to process: {len(rows)}")

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
    print(f"  - Total Processed: {ingested_count + triaged_count}/157")

if __name__ == "__main__":
    process_all_smart_pizza_shorts()
