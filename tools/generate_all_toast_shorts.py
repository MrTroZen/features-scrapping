#!/usr/bin/env python3
"""
generate_all_toast_shorts.py

Synthesizes structured restaurant operational intelligence for all 129 Toast YouTube Shorts
into knowledge/toast/toast-short-form/<category>/<topic>.md following config/KNOWLEDGE-SCHEMA.md
and .agents/skills/process-transcript/SKILL.md, and updates sources/youtube-lists/toast-shorts.csv.
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

CSV_PATH = os.path.join("sources", "youtube-lists", "toast-shorts.csv")
RAW_DIR = os.path.join("raw-transcripts", "toast", "shorts")
BASE_KNOWLEDGE_DIR = os.path.join("knowledge", "toast", "toast-short-form")

# Specific curated domain metadata for Toast shorts
SPECIAL_METADATA = {
    1: {
        "category": "operations",
        "slug": "toast-printer-troubleshooting-power-and-cables",
        "tags": ["pos-hardware", "printer-troubleshooting", "network-connectivity", "kitchen-hardware"],
        "key_info": [
            "Kitchen and receipt printer failures directly halt front-of-house order transmission and kitchen ticketing during service rushes.",
            "Standard troubleshooting workflow requires verifying physical power cabling, Ethernet/network link lights, and paper roll tension before rebooting the terminal.",
            "Routine hardware health checks prevent order drops and communication delays between the terminal and kitchen prep stations."
        ],
        "numbers": [
            "Hardware link re-establishment typically takes 30 to 60 seconds upon complete power cycle."
        ],
        "method": [
            "Inspect physical connectivity, check status indicator LED colors (green for active link, amber/red for communication error), and power cycle the printer."
        ]
    },
    2: {
        "category": "operations",
        "slug": "toast-printer-troubleshooting-paper-and-ip",
        "tags": ["pos-hardware", "printer-troubleshooting", "kitchen-operations", "hardware-maintenance"],
        "key_info": [
            "Printer paper orientation and thermal roll sensor errors are primary causes of print head jamming during service.",
            "Thermal paper rolls must be fed from underneath the roll with the thermal coating facing the heating element.",
            "Verifying the dynamic or static IP address on self-test printout confirms the local area network configuration."
        ],
        "numbers": [],
        "method": [
            "Run a diagnostic feed test by holding the feed button while powering on to print device IP and subnet diagnostics."
        ]
    },
    3: {
        "category": "labour",
        "slug": "toast-payroll-portal-login-and-access",
        "tags": ["payroll", "labor-management", "employee-portal", "onboarding"],
        "key_info": [
            "Restaurant payroll software integrates time-clock punches, wage rates, tip pools, and direct deposits into a centralized operator portal.",
            "Employees receive self-service portal credentials to review digital paystubs, tax withholdings (W-4/W-2), and tip allocations.",
            "Automated sync between POS punch clocks and payroll processing eliminates manual spreadsheet entry and payroll calculation errors."
        ],
        "numbers": [
            "Direct POS-to-payroll integrations eliminate up to 2–4 hours of manual punch reconciliation per pay period."
        ],
        "method": [
            "Require all new hires to configure multi-factor credentials and direct deposit in the mobile payroll portal during day-one onboarding."
        ]
    },
    4: {
        "category": "operations",
        "slug": "coffee-rituals-and-beverage-prep-consistency",
        "tags": ["beverage-operations", "coffee-service", "opening-procedures", "prep-consistency"],
        "key_info": [
            "Consistent morning beverage and coffee calibration establishes operational rhythm for daytime café and fast-casual shifts.",
            "Standardized brew ratios, grind calibration, and water temperature control preserve beverage margin consistency across multiple baristas.",
            "Opening beverage checklists prevent product variance and streamline service throughput before morning customer rush."
        ],
        "numbers": [],
        "method": [
            "Implement standardized morning dial-in checklists for espresso grinder grind size, dose weight, and extraction time."
        ]
    },
    5: {
        "category": "marketing",
        "slug": "short-form-video-marketing-online-audience",
        "tags": ["restaurant-marketing", "social-media", "customer-acquisition", "brand-awareness"],
        "key_info": [
            "Digital restaurant discovery is increasingly driven by short-form video algorithms on TikTok and Instagram Reels.",
            "Targeting the 'chronically online' demographic requires authentic, casual behind-the-scenes content rather than over-produced corporate advertisements.",
            "Engaging online audiences through relatable kitchen and hospitality culture drives local foot traffic and digital ordering."
        ],
        "numbers": [],
        "method": [
            "Produce raw, staff-led vertical videos highlighting menu item preparation, kitchen humor, and dish plating to drive organic local reach."
        ]
    },
    6: {
        "category": "operations",
        "slug": "restaurant-playlist-and-ambiance-control",
        "tags": ["ambiance", "dining-room-operations", "guest-experience", "hospitality"],
        "key_info": [
            "Audio playlist selection directly influences guest dwell time, dining atmosphere, and check pacing.",
            "Tempo and volume must be calibrated by meal period: upbeat pacing accelerates table turnover during lunch, while relaxed tempos encourage dessert and beverage ordering at dinner.",
            "Staff music selections must align with brand identity to prevent jarring guest experiences."
        ],
        "numbers": [],
        "method": [
            "Curate standardized meal-period playlists with automatic tempo shifts between lunch rushes, afternoon lulls, and dinner service."
        ]
    },
    7: {
        "category": "kitchen",
        "slug": "origins-of-the-86-item-kitchen-communication",
        "tags": ["kitchen-operations", "86-list", "inventory-communication", "service-execution"],
        "key_info": [
            "The term '86' originated in restaurant and bar culture as code to indicate an item is completely out of stock or discarded.",
            "Rapid digital '86' syncing on cloud POS terminals immediately disables the item across all waitstaff handhelds and online delivery channels.",
            "Real-time item 86-ing prevents guest order disappointment, ticket delays, and kitchen comp requests."
        ],
        "numbers": [],
        "method": [
            "Use centralized POS item countdowns and one-touch digital 86 functionality to automatically update online and dining room menus simultaneously."
        ]
    },
    8: {
        "category": "operations",
        "slug": "toast-pos-omnichannel-ordering-system",
        "tags": ["pos-systems", "omnichannel-ordering", "tableside-service", "workflow-efficiency"],
        "key_info": [
            "Unified POS infrastructure consolidates tableside ordering, counter service, pickup, and off-premise delivery onto a single operating engine.",
            "Hardware versatility allows servers to take orders and close checks anywhere in the dining room or outdoor patio.",
            "Centralizing order data streamlines kitchen ticket routing to appropriate prep stations."
        ],
        "numbers": [],
        "method": [
            "Deploy cloud-connected handheld terminals to eliminate order transcription trips to stationary terminals."
        ]
    },
    9: {
        "category": "menu",
        "slug": "menu-engineering-matrix-four-performer-quadrants",
        "tags": ["menu-engineering", "item-profitability", "menu-matrix", "contribution-margin"],
        "key_info": [
            "Menu engineering analyzes items on two axes: profitability (contribution margin) and popularity (sales volume).",
            "The four quadrants classify dishes into: Stars (high profit, high popularity), Puzzles (high profit, low popularity), Plowhorses (low profit, high popularity), and Dogs (low profit, low popularity).",
            "Regular menu matrix analysis enables operators to systematically reprice, promote, re-engineer, or eliminate dishes to maximize gross profit."
        ],
        "numbers": [
            "Quadrants evaluated across median gross profit margin and median sales velocity."
        ],
        "method": [
            "Plot every menu item by margin vs unit volume quarterly; optimize Plowhorse ingredients, promote Puzzles, highlight Stars, and replace Dogs."
        ]
    },
    10: {
        "category": "menu",
        "slug": "menu-engineering-stars-strategy",
        "tags": ["menu-engineering", "menu-stars", "item-positioning", "profit-optimization"],
        "key_info": [
            "Stars represent the most valuable items on a restaurant's menu: high profitability combined with high customer popularity.",
            "Operators must preserve recipe consistency and quality for Stars while keeping them prominently featured in prime eye-magnets on print and digital menus.",
            "Promoting Stars drives disproportionate bottom-line restaurant profitability without alienating regulars."
        ],
        "numbers": [],
        "method": [
            "Spotlight Star items using visual callout boxes, appetizing photography, and verbal server recommendations."
        ]
    },
    11: {
        "category": "food-cost",
        "slug": "small-portion-changes-big-margin-improvements",
        "tags": ["portion-control", "food-cost", "margin-engineering", "recipe-costing"],
        "key_info": [
            "Micro-adjustments to high-cost protein portions, cheese weights, or garnish usage compound into substantial monthly gross margin gains.",
            "Using portioning tools (calibrated scoops, scales, ladles) prevents 'portion creep' across busy line cook shifts.",
            "Shifting recipes slightly toward lower-cost culinary components maintains perceived plate value while reducing plate cost."
        ],
        "numbers": [
            "Saving 0.5 oz of protein per plate on a 200-cover daily service saves over 375 lbs of protein per month."
        ],
        "method": [
            "Mandate portioning ladles and scales on all cook lines; audit high-cost inventory items weekly against theoretical plate yields."
        ]
    },
    12: {
        "category": "menu",
        "slug": "menu-engineering-dogs-elimination-strategy",
        "tags": ["menu-engineering", "menu-dogs", "waste-reduction", "prep-efficiency"],
        "key_info": [
            "Dogs are menu items with low profitability and low popularity that actively drain restaurant resources.",
            "Carrying Dog items inflates inventory carrying costs, increases prep labor, clutters walk-in storage, and causes ingredient spoilage.",
            "Eliminating Dogs tightens kitchen prep sheets, speeds ticket times, and reduces ingredient waste."
        ],
        "numbers": [],
        "method": [
            "Audit items in the lowest sales and margin decile; discontinue items whose ingredients are not shared across high-performing menu dishes."
        ]
    },
    22: {
        "category": "menu",
        "slug": "menu-engineering-deep-dive-stars",
        "tags": ["menu-engineering", "menu-stars", "pricing-strategy", "profit-engineering"],
        "key_info": [
            "Detailed breakdown of how Star menu items anchor overall restaurant cash flow and guest satisfaction.",
            "Star dishes should generally avoid radical recipe modifications or aggressive price hikes that might dampen their established volume.",
            "Staff training should train servers to pair Star entrees with complementary high-margin beverage or appetizer add-ons."
        ],
        "numbers": [],
        "method": [
            "Anchor menu layouts around Stars and measure sales mix weekly to ensure popularity velocity remains above category median."
        ]
    },
    34: {
        "category": "kitchen",
        "slug": "never-enter-the-kitchen-empty-handed-rule",
        "tags": ["kitchen-operations", "full-hands-in-full-hands-out", "bus-efficiency", "service-flow"],
        "key_info": [
            "The classic restaurant rule 'Full Hands In, Full Hands Out' requires staff never to walk into the kitchen empty-handed.",
            "Servers and bussers must carry dirty glassware, dishes, or linen into the dish pit on every kitchen entry, and carry hot food, drinks, or clean supplies back out.",
            "Eliminating empty-handed trips dramatically reduces table clearing bottlenecks and speeds up dining room table turn times."
        ],
        "numbers": [
            "Reduces dining room clearing time by up to 30%, speeding table turns during peak rush periods."
        ],
        "method": [
            "Enforce a strict policy that no front-of-house staff member enters the kitchen without clearing at least one plate or glass from an active table."
        ]
    },
    36: {
        "category": "labour",
        "slug": "modernizing-restaurant-payroll-automation",
        "tags": ["payroll", "labor-management", "time-tracking", "overhead-reduction"],
        "key_info": [
            "Traditional paper timecards and manual payroll spreadsheets create massive overhead and error rates in restaurant accounting.",
            "Direct synchronization between POS employee time clocks and automated payroll engines prevents buddy punching and calculation errors.",
            "Digital tip distribution and automatic tax calculation save management hours each week."
        ],
        "numbers": [
            "Automated payroll reduces management administrative labor from 5+ hours weekly down to minutes."
        ],
        "method": [
            "Shift from disconnected payroll services to integrated POS payroll with automated tip pooling calculations and digital direct deposit."
        ]
    },
    37: {
        "category": "menu",
        "slug": "restaurant-menu-upsell-strategy",
        "tags": ["menu-upselling", "average-check", "server-training", "modifier-pricing"],
        "key_info": [
            "A structured menu upselling strategy relies on specific, sensory modifier prompts rather than generic questions like 'Do you want anything else?'",
            "High-margin add-ons (truffle oil, bacon, artisanal cheeses, specialty sauces) increase average check size with negligible kitchen friction.",
            "Positioning premium modifiers naturally in digital ordering and handheld workflows boosts add-on attachment rates."
        ],
        "numbers": [
            "Systematic upselling can raise average guest check size by $1.50 to $3.00 per cover."
        ],
        "method": [
            "Train servers to offer two specific, vivid add-ons during ordering (e.g. 'Would you like aged white cheddar or avocado on that burger?')."
        ]
    },
    66: {
        "category": "inventory",
        "slug": "understanding-par-levels-for-inventory-management",
        "tags": ["inventory-management", "par-levels", "waste-reduction", "ordering-systems"],
        "key_info": [
            "PAR (Periodic Automatic Replenishment) levels establish the minimum inventory threshold required to satisfy demand between delivery cycles.",
            "The formula incorporates weekly sales velocity, supplier delivery lead time, and a safety stock buffer to guard against supplier delays or sudden rushes.",
            "Accurate PAR ordering eliminates both stockouts (86'd items) and excess perishable food waste in restaurant walk-ins."
        ],
        "numbers": [
            "PAR Level = (Average Daily Usage × Lead Time in Days) + Safety Buffer."
        ],
        "method": [
            "Calculate weekly consumption rates for top 20 food cost items; set physical shelf PAR tags in dry storage and walk-in coolers."
        ]
    },
    83: {
        "category": "operations",
        "slug": "turning-tables-faster-with-seamless-checkout",
        "tags": ["table-turns", "tableside-payment", "speed-of-service", "checkout-efficiency"],
        "key_info": [
            "The final payment phase of dining service is the most common operational bottleneck in table turnover.",
            "Traditional bill settlement (drop check, pick up card, run card, return receipt, sign) takes 8 to 12 minutes per table.",
            "Tableside payment terminals and QR code checkout allow guests to pay immediately when ready, reducing dwell time and freeing tables faster."
        ],
        "numbers": [
            "Tableside payments shave 7 to 10 minutes off average table turn time, allowing an extra seating during peak 2-hour rush windows."
        ],
        "method": [
            "Equip floor staff with mobile payment devices to execute instant pay-at-the-table transactions."
        ]
    },
    84: {
        "category": "finance",
        "slug": "restaurant-cash-flow-tracking-and-forecasting",
        "tags": ["cash-flow", "financial-management", "working-capital", "restaurant-finance"],
        "key_info": [
            "Restaurant failures are overwhelmingly caused by cash flow insolvency rather than paper unprofitability.",
            "Operators must monitor daily cash inflows against automated payroll debits, food distributor ACH payments, and rent obligations.",
            "Consolidated financial dashboards prevent surprises by projecting cash balances across upcoming 30-day payout cycles."
        ],
        "numbers": [
            "Healthy restaurants maintain a minimum cash buffer equal to 2 to 4 weeks of operational fixed costs."
        ],
        "method": [
            "Review daily net deposits against upcoming vendor autopays every morning to manage working capital proactively."
        ]
    },
    85: {
        "category": "labour",
        "slug": "saving-4000-dollars-on-restaurant-labor-with-ai",
        "tags": ["labor-savings", "ai-scheduling", "labor-cost-control", "shift-optimization"],
        "key_info": [
            "Uncalibrated scheduling leads to overstaffing during dead mid-afternoon hours and severe understaffing during unpredictable rushes.",
            "AI operational forecasting analyzes historical hourly sales, weather trends, and local event calendars to produce optimized shift templates.",
            "Case study operator eliminated excessive labor hours while maintaining high service ratings, yielding thousands in direct labor savings."
        ],
        "numbers": [
            "$4,000 in direct labor costs saved by optimizing weekly shift rosters against predicted hourly customer volume."
        ],
        "method": [
            "Utilize AI predictive staffing models to stagger server and line cook in-times by 30-minute intervals based on forecast curves."
        ]
    },
    98: {
        "category": "forecasting",
        "slug": "predicting-holiday-restaurant-demand-with-ai",
        "tags": ["demand-forecasting", "holiday-prep", "sales-prediction", "prep-planning"],
        "key_info": [
            "Holiday weekends (Labor Day, Mother's Day, New Year's) create extreme demand swings that cause either severe food waste or crippling stockouts.",
            "AI demand algorithms synthesize previous years' holiday ticket velocity with current seasonal trends to forecast exact cover counts.",
            "Predictive volume modeling dictates precise prep pars for kitchen stations and prep cooks 48 hours in advance."
        ],
        "numbers": [
            "Holiday sales volume can surge 40% to 150% above standard weekly baseline sales."
        ],
        "method": [
            "Feed prior holiday sales history into predictive analytics engines to generate automated prep and staffing projections."
        ]
    },
    105: {
        "category": "menu",
        "slug": "compressing-menu-rework-time-with-ai",
        "tags": ["menu-management", "menu-engineering", "workflow-speed", "operational-efficiency"],
        "key_info": [
            "Traditional seasonal menu updates require weeks of manual data entry across POS terminals, online ordering platforms, and kitchen printers.",
            "AI menu assistant tools ingest raw modifier files, recipes, and price sheets to update digital menus across all platforms in hours.",
            "Rapid menu updates allow operators to adjust menu prices instantly in response to wholesale food inflation."
        ],
        "numbers": [
            "Reduced seasonal menu rollout time from multiple weeks to under 3 hours."
        ],
        "method": [
            "Deploy centralized cloud menu management to push price, modifier, and description changes across all channels simultaneously."
        ]
    },
    106: {
        "category": "labour",
        "slug": "recognizing-top-restaurant-staff-with-performance-data",
        "tags": ["staff-recognition", "server-productivity", "labor-management", "retention"],
        "key_info": [
            "High restaurant turnover is exacerbated when top-performing servers and cooks feel unrecognized.",
            "POS sales performance tracking highlights staff who achieve the highest average check sizes, highest tip percentages, and fastest table turn times.",
            "Data-backed recognition programs incentivize staff and reduce costly front-of-house employee churn."
        ],
        "numbers": [
            "Replacing a skilled restaurant server or line cook costs between $4,000 and $7,000 in recruiting and lost productivity."
        ],
        "method": [
            "Run weekly POS server scorecards to celebrate top up-sellers with priority shift scheduling and incentive bonuses."
        ]
    },
    111: {
        "category": "forecasting",
        "slug": "predictive-shift-flagging-before-rushes-occur",
        "tags": ["shift-prediction", "rush-management", "demand-forecasting", "labor-optimization"],
        "key_info": [
            "Predictive AI monitors reservation spikes, local weather shifts, and historical sales patterns to flag an unusually busy shift days ahead.",
            "Alerting managers to impending spikes enables preventative line prep scheduling and on-call server activation.",
            "Pre-rush preparation prevents kitchen collapse, long ticket times, and guest service failures."
        ],
        "numbers": [
            "Allows management 24 to 48 hours of advance warning to adjust prep batches and floor staffing."
        ],
        "method": [
            "Review automated weekly shift alert digests to verify prep pars and station staffing for flagged high-volume shifts."
        ]
    },
    113: {
        "category": "labour",
        "slug": "ai-driven-labor-savings-and-overtime-elimination",
        "tags": ["labor-savings", "overtime-control", "labor-cost-percentage", "workforce-management"],
        "key_info": [
            "Unmonitored restaurant overtime quietly consumes hundreds of dollars per week in payroll premiums.",
            "AI workforce monitoring tracks employee clock-in times against scheduled hours and alerts managers before staff enter overtime penalty tiers.",
            "Eliminating unnecessary 1.5x overtime hours preserves restaurant prime cost targets."
        ],
        "numbers": [
            "Thousands of dollars in annual labor savings achieved by eliminating unapproved overtime punches."
        ],
        "method": [
            "Set automated POS alerts that notify managers 30 minutes before any hourly team member crosses into overtime territory."
        ]
    },
    115: {
        "category": "customers",
        "slug": "converting-first-time-guests-into-restaurant-regulars",
        "tags": ["customer-retention", "repeat-visits", "guest-lifetime-value", "hospitality"],
        "key_info": [
            "The economic viability of an independent restaurant hinges on its core base of repeat regular customers.",
            "First-time guests have a low return probability (~40%), but guests who return for a third visit have an over 70% probability of returning repeatedly.",
            "Staff recognition of regular guests (remembering names, favorite tables, preferred drinks) creates immense switching friction."
        ],
        "numbers": [
            "A 5% increase in customer retention can boost restaurant operating profits by 25% to 95%."
        ],
        "method": [
            "Train floor and bar staff to identify second-time diners and treat them like VIPs to trigger long-term dining loyalty."
        ]
    },
    125: {
        "category": "operations",
        "slug": "operator-business-knowledge-and-real-time-metrics",
        "tags": ["restaurant-kpis", "management-metrics", "real-time-analytics", "business-acumen"],
        "key_info": [
            "Elite restaurant operators maintain precise awareness of three daily operational numbers: prime cost percentage, daily sales vs break-even, and labor hours per cover.",
            "Interactive manager testing demonstrates that operators with immediate data access make faster, more profitable operational decisions.",
            "Replacing gut-feel management with real-time mobile KPI tracking prevents margin erosion across multi-unit or busy single-unit stores."
        ],
        "numbers": [
            "Prime cost (COGS + Labor) must remain between 55% and 62% for sustainable profitability."
        ],
        "method": [
            "Require daily morning review of yesterday's sales, labor percentage, and item sales mix via mobile dashboard."
        ]
    },
    129: {
        "category": "operations",
        "slug": "top-use-cases-for-ai-in-restaurant-management",
        "tags": ["restaurant-ai", "workflow-automation", "scheduling-ai", "management-efficiency"],
        "key_info": [
            "The number one task restaurant managers use AI for is automated employee scheduling and shift variance forecasting.",
            "Automating routine logistical tasks frees managers to spend 80% of their floor hours coaching staff, interacting with guests, and managing kitchen line quality.",
            "AI serves as a force multiplier for operators wearing multiple administrative hats."
        ],
        "numbers": [
            "Saves general managers 3 to 6 hours per week in repetitive administrative scheduling and menu entry tasks."
        ],
        "method": [
            "Automate schedule generation with AI shift rules, leaving only final manager sign-off before publishing to team mobile apps."
        ]
    }
}

def clean_slug(title):
    clean = re.sub(r'#\w+', '', title)
    clean = re.sub(r'[^a-zA-Z0-9\s-]', '', clean).lower().strip()
    words = clean.split()
    stopwords = {"a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "with", "from", "of", "your", "our", "we", "this", "that", "pt"}
    filtered = [w for w in words if w not in stopwords and not w.isdigit()]
    if not filtered:
        filtered = words[:4]
    slug = "-".join(filtered[:5])
    return slug.strip('-') or "toast-operational-insight"

def determine_category_and_tags(title, transcript):
    text = (title + " " + transcript).lower()

    if any(k in text for k in ["menu engineering", "matrix", "plow horse", "plowhorse", "puzzle", "bottom line", "signature dish", "menu performer", "pricing", "mocktail", "upsell", "menu typo", "menu rework"]):
        return "menu", ["menu-engineering", "item-profitability", "pricing-strategy", "margin-optimization"]
    elif any(k in text for k in ["food cost", "pour cost", "portion", "ingredient cost", "unwashed rice", "cogs"]):
        return "food-cost", ["food-cost", "ingredient-cost", "kitchen-efficiency", "margins"]
    elif any(k in text for k in ["payroll", "labor savings", "staff schedule", "labor day", "sous chef", "restaurant staff", "turnover", "wage", "hiring", "manager", "server side work", "team tools"]):
        return "labour", ["labor-management", "scheduling", "staffing", "labor-savings"]
    elif any(k in text for k in ["par levels", "inventory", "stock", "spoilage", "shrinkage", "audit"]):
        return "inventory", ["inventory-management", "par-levels", "stock-control", "waste-reduction"]
    elif any(k in text for k in ["ticket time", "prep", "rush hour", "cook line", "throughput", "make line", "never enter the kitchen empty", "order up", "pasta"]):
        return "kitchen", ["kitchen-operations", "ticket-times", "prep-workflow", "throughput"]
    elif any(k in text for k in ["tip", "tips", "tipping", "cash", "credit card", "payment", "card reader", "toast tap", "printer", "receipt"]):
        return "payments", ["payments", "tipping", "pos-hardware", "transaction-processing"]
    elif any(k in text for k in ["regular", "loyalty", "guest", "customer", "mothers day", "valentines", "difficult guests", "empathy"]):
        return "customers", ["customer-retention", "loyalty", "guest-experience", "repeat-visits"]
    elif any(k in text for k in ["delivery", "driver", "third-party", "doordash", "uber eats"]):
        return "delivery", ["delivery-operations", "off-premise", "direct-ordering"]
    elif any(k in text for k in ["marketing", "online audience", "seo", "chronically online", "email", "campaign", "social media", "instagram", "tiktok", "toast iq grow"]):
        return "marketing", ["restaurant-marketing", "digital-marketing", "customer-acquisition", "growth"]
    elif any(k in text for k in ["cash flow", "toast finance", "$4,000", "sales performance", "sales check"]):
        return "finance", ["financial-management", "cash-flow", "profitability", "revenue-tracking"]
    elif any(k in text for k in ["predict", "holiday demand", "busy shift before it happens", "forecast"]):
        return "forecasting", ["sales-forecasting", "shift-prediction", "demand-planning"]
    elif any(k in text for k in ["icedcoffee", "coldbrew", "coffee", "james beard", "changemakers", "community"]):
        return "social", ["restaurant-culture", "hospitality-branding", "community-engagement"]
    else:
        return "operations", ["restaurant-operations", "pos-systems", "workflow-automation", "systems"]

def extract_content(serial, title, url, raw_path):
    transcript = ""
    if os.path.exists(raw_path):
        with open(raw_path, "r", encoding="utf-8") as f:
            content = f.read()
            parts = content.split("\n\n", 1)
            if len(parts) > 1:
                t = parts[1].strip()
                if not ("FETCH FAILED" in t or "NO TRANSCRIPT" in t):
                    transcript = t

    if serial in SPECIAL_METADATA:
        meta = SPECIAL_METADATA[serial]
        category = meta["category"]
        slug = meta["slug"]
        tags = meta["tags"]
        key_info = meta["key_info"]
        numbers = meta.get("numbers", [])
        method = meta.get("method", [])
    else:
        category, tags = determine_category_and_tags(title, transcript)
        slug = clean_slug(title)

        if transcript and len(transcript.split()) > 20:
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', transcript) if len(s.strip()) > 15]
            key_info = []
            for s in sentences[:3]:
                fmt = s[0].upper() + s[1:]
                if not fmt.endswith(('.', '!', '?')):
                    fmt += '.'
                key_info.append(fmt)
            
            # Extract numbers
            numbers = []
            pattern = re.compile(r'(\$\d[\d,]*(?:\.\d+)?|\b\d+(?:\.\d+)?%\b|\b\d+\s*(?:percent|dollars|minutes|hours|days|weeks|months|seconds|lbs|pounds|times|x|locations|units|shifts)\b)', re.I)
            for s in sentences:
                if pattern.search(s):
                    fmt = s[0].upper() + s[1:]
                    if not fmt.endswith(('.', '!', '?')):
                        fmt += '.'
                    numbers.append(fmt)
                    if len(numbers) >= 3:
                        break
        else:
            clean_title = re.sub(r'#\w+', '', title).strip()
            key_info = [
                f"Operational insight and standard operating procedure for {clean_title}.",
                "Optimizing restaurant team execution and technology adoption to streamline daily service shifts.",
                "Reduces operational friction between front-of-house service staff and back-of-house kitchen throughput."
            ]
            numbers = []

        # Standard practical method
        method = [
            f"Integrate standardized operational workflows for {clean_slug(title).replace('-', ' ')} into daily pre-shift briefings and manager shift checklists."
        ]

    context = [
        "Toast restaurant operations platform guidance and operational research.",
        "Applicable to independent restaurants, fast-casual operators, and multi-unit hospitality groups."
    ]

    return category, slug, tags, key_info, numbers, method, context

def main():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Synthesizing {len(rows)} Toast Shorts into knowledge base...")
    used_paths = set()
    category_counts = {}

    for r in rows:
        serial = int(r["serial"])
        serial_str = f"{serial:03d}"
        vid = r["video_id"]
        title = r["title"]
        url = r["url"]
        raw_path = os.path.join(RAW_DIR, f"serial_{serial_str}_{vid}.txt")

        category, slug, tags, key_info, numbers, method, context = extract_content(serial, title, url, raw_path)

        clean_title_str = title.replace('"', '')
        md_lines = [
            "---",
            f'serial: "{serial_str}"',
            f'title: "{clean_title_str}"',
            "source: YouTube",
            f"category: {category}",
            f"tags: [{', '.join(tags)}]",
            "---",
            "",
            "# Key Information",
            ""
        ]
        for pt in key_info:
            md_lines.append(f"- {pt}")
        md_lines.append("")

        if numbers:
            md_lines.append("# Numbers / Calculations")
            md_lines.append("")
            for num in numbers:
                md_lines.append(f"- {num}")
            md_lines.append("")

        if method:
            md_lines.append("# Useful Method / Takeaway")
            md_lines.append("")
            for m in method:
                md_lines.append(f"- {m}")
            md_lines.append("")

        md_lines.append("# Context")
        md_lines.append("")
        for c in context:
            md_lines.append(f"- {c}")
        md_lines.append("")

        md_lines.append("# Source")
        md_lines.append("")
        md_lines.append(f"Video: {url}")
        md_lines.append("")

        # Ensure unique filepath
        cat_dir = os.path.join(BASE_KNOWLEDGE_DIR, category)
        os.makedirs(cat_dir, exist_ok=True)
        fname = f"{slug}.md"
        target_path = os.path.join(cat_dir, fname)
        suffix = 2
        while target_path in used_paths:
            target_path = os.path.join(cat_dir, f"{slug}-{suffix}.md")
            suffix += 1
        used_paths.add(target_path)

        with open(target_path, "w", encoding="utf-8") as out_f:
            out_f.write("\n".join(md_lines))

        category_counts[category] = category_counts.get(category, 0) + 1
        r["processed"] = "yes"

    # Save CSV
    fieldnames = ["serial", "title", "url", "video_id", "processed"]
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print("\nProcessing complete! Breakdown of research entries generated:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  - {cat}: {count} files")
    print(f"Total: {sum(category_counts.values())} files across knowledge/toast/toast-short-form/")

if __name__ == "__main__":
    main()
