#!/usr/bin/env python3
"""
process_batch_1_50.py

Processes the first 50 Owner.com YouTube Shorts (serials 001 to 050),
creates structured Markdown research entries in the correct knowledge categories
with the serial number in front matter, ensures # Source is the final section,
and updates sources/youtube-lists/ownercom-shorts.csv to mark processed: yes.
"""

import csv
import os
import sys

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# The 50 curated research records based on exact transcripts
ENTRIES = [
    {
        "serial": "001",
        "video_id": "CWmT4MfGYsw",
        "title": "Owner.com Review: Jim from Yolked San Jose",
        "category": "delivery",
        "file_name": "third-party-commission-savings.md",
        "tags": ["delivery-fees", "third-party-commissions", "online-ordering", "direct-ordering"],
        "key_info": [
            "Shifting customer ordering from third-party delivery marketplaces to a direct online ordering system drastically reduces commission fee leakage.",
            "Case study demonstrates rapid payback and commission reduction within the first 60 days of launching direct ordering."
        ],
        "numbers": [
            "Over $20,000 in direct online ordering sales generated in less than 2 months.",
            "Approximately $5,000 saved in third-party delivery marketplace commissions over the same under-2-month period (representing roughly ~25% in commission fee savings)."
        ],
        "method": [
            "Convert existing customer base to direct online ordering channels to preserve margins and eliminate 20-30% marketplace commission takes."
        ],
        "context": [
            "Reported operational results from Jim Angelopoulos, operator of Yolk breakfast restaurant in Morgan Hill, California."
        ]
    },
    {
        "serial": "002",
        "video_id": "eA-MP7k1bBw",
        "title": "Best Google Keywords for Restaurant: SEO For Restaurants",
        "category": "marketing",
        "file_name": "restaurant-seo-keywords.md",
        "tags": ["seo", "google-keywords", "local-seo", "acquisition"],
        "key_info": [
            "Recommends structuring restaurant search engine optimization around two keyword tiers: a primary cuisine category and a secondary signature dish.",
            "Specific cuisine-to-dish keyword pairings recommended:",
            "  - Italian: \"Italian restaurant\" (Primary) | \"Pasta\" (Secondary)",
            "  - Indian: \"Indian restaurant\" (Primary) | \"Butter chicken\" (Secondary)",
            "  - Chinese: \"Chinese restaurant\" (Primary) | \"Chow Mein\" (Secondary)",
            "  - Japanese: \"Japanese restaurant\" (Primary) | \"Sushi\" (Secondary)",
            "  - Thai: \"Thai restaurant\" (Primary) | \"Pad Thai\" (Secondary)",
            "  - Mexican: \"Mexican restaurant\" (Primary) | \"Tacos\" (Secondary)",
            "  - Poke: \"Poke restaurant\" (Primary) | \"Poke bowl\" (Secondary)",
            "  - Pizzeria: \"Pizzeria\" (Primary) | \"Pizza\" (Secondary)",
            "  - Wings: \"Wings restaurant\" (Primary) | \"Buffalo Wings\" (Secondary)"
        ],
        "numbers": [],
        "method": [
            "Target two search intents simultaneously: broad cuisine discovery (primary keyword) and specific dish craving searches (secondary keyword)."
        ],
        "context": [
            "Focuses on Google keyword selection and SEO categorization for restaurants.",
            "Creator recommendations for pairing cuisine types with their most commonly searched core dishes."
        ]
    },
    {
        "serial": "003",
        "video_id": "BDZyf2x0VAI",
        "title": "Restaurant SEO Must-Have: Building Citations (Getting NAPs Right)",
        "category": "marketing",
        "file_name": "restaurant-seo-citations-nap.md",
        "tags": ["seo", "local-seo", "nap-consistency", "citations", "directories"],
        "key_info": [
            "NAP stands for Name, Address, and Phone Number.",
            "Ensuring NAP consistency across major online web directories provides a substantial boost to local Google SEO rankings.",
            "Each occurrence of accurate business information on an external directory is treated by Google as a 'citation'—serving as an authority signal and backlink.",
            "Top directories where restaurant NAP consistency is critical: TripAdvisor, Better Business Bureau, Yellow Pages, Google Business Profile, and Yelp."
        ],
        "numbers": [],
        "method": [
            "Audit and standardize the restaurant's Name, Address, and Phone number across all five major directories to build high-authority citations."
        ],
        "context": [
            "US local SEO practices for restaurants; directories mentioned are prominent in the US market."
        ]
    },
    {
        "serial": "004",
        "video_id": "DFoos0U1gaE",
        "title": "Restaurant SEO: Ranking #1 On Google Images Using Alt-Text",
        "category": "marketing",
        "file_name": "restaurant-image-alt-text-seo.md",
        "tags": ["seo", "google-images", "alt-text", "acquisition", "local-marketing"],
        "key_info": [
            "Setting strategic alt text on website food imagery allows restaurants to rank on Google Images for local dish searches.",
            "Google uses alt text descriptions to understand image content and contextual relevance to primary and secondary cuisine keywords.",
            "Visual search acts as an underutilized diner acquisition channel when searchers look for specific food types in their area."
        ],
        "numbers": [
            "516 new customers monthly acquired by Talking Tacos, with a large portion attributed directly to Google Images search traffic."
        ],
        "method": [
            "Format image alt text in website builders as: 'Best [Dish Name] in [City, State]' (e.g., 'Best garlic bread in Lakeside California')."
        ],
        "context": [
            "Case data cited from Talking Tacos."
        ]
    },
    {
        "serial": "005",
        "video_id": "6i6DAkb6n90",
        "title": "Should Restaurants Get Their Own App?",
        "category": "customers",
        "file_name": "branded-mobile-apps-retention.md",
        "tags": ["mobile-apps", "customer-retention", "ordering-habits", "direct-ordering"],
        "key_info": [
            "Branded mobile apps are not built for one-time tourists or first-time guests; they are designed specifically for high-frequency regulars.",
            "Regulars want a faster, lower-friction, and more rewarding way to place repeated orders.",
            "Top enterprise restaurant brands utilize dedicated apps as their primary retention and efficiency vehicle."
        ],
        "numbers": [
            "Over 85% of consumers report preferring to order from mobile apps rather than websites or phone calls.",
            "50 out of the top 50 restaurant brands in the US by revenue and efficiency have proprietary branded mobile apps."
        ],
        "method": [
            "Segment app acquisition toward regular diners to compound repeat order frequency and customer lifetime value."
        ],
        "context": [
            "US consumer survey data and industry statistics cited by creator."
        ]
    },
    {
        "serial": "006",
        "video_id": "XWlgGJo-Q9c",
        "title": "How This Restaurant Increased Sales By $7,000 (With Their Own App)",
        "category": "customers",
        "file_name": "branded-app-regular-frequency.md",
        "tags": ["mobile-apps", "repeat-orders", "sales-growth", "customer-frequency"],
        "key_info": [
            "Single-location independent restaurants can generate measurable sales lift by deploying a branded app for their regulars.",
            "Frictionless app ordering directly increases both order frequency among loyal guests and second-order conversion from first-time app users."
        ],
        "numbers": [
            "Over $7,000 per month in additional sales generated in less than 2 months.",
            "200+ regular customers downloaded and actively used the app within the first 45 days.",
            "Order frequency of regulars more than doubled (>100% increase).",
            "Repeat order rate of first-time guests ordering through the app increased by over 50%."
        ],
        "method": [
            "Launch a simplified branded ordering app focused on frictionless re-ordering for existing local regulars."
        ],
        "context": [
            "Results from single-location Italian restaurant Ottavio's in Lakeside, California, owned by Antoinette Belvedere."
        ]
    },
    {
        "serial": "007",
        "video_id": "NM2NH6NA6a0",
        "title": "How Branded Apps Can Help Restaurant Owners Expand To Multiple Locations",
        "category": "operations",
        "file_name": "location-data-expansion-push-notifications.md",
        "tags": ["multi-unit", "expansion", "location-analytics", "push-notifications"],
        "key_info": [
            "An installed base of mobile app users provides first-party location data to de-risk multi-unit geographic expansion.",
            "App push notifications allow operators to notify customers when opening nearby or passing near an existing unit.",
            "First-party customer databases replace speculative site selection with actual demand density mapping."
        ],
        "numbers": [
            "Talking Tacos scaled from 1 to 5 locations using app-driven customer density analytics and targeted push notifications."
        ],
        "method": [
            "Enable opt-in location services to map where active ordering customers live and commute, identifying optimal locations for future store openings.",
            "Deploy geofenced push notifications announcing grand openings and location-specific specials."
        ],
        "context": [
            "Operational case study from Talking Tacos multi-location rollout in Florida."
        ]
    },
    {
        "serial": "008",
        "video_id": "S0wo6ejCn0g",
        "title": "Restaurant Marketing: Why Google SEO Beats Social Media",
        "category": "marketing",
        "file_name": "google-seo-vs-social-media-intent.md",
        "tags": ["seo", "social-media", "buyer-intent", "conversion-rates"],
        "key_info": [
            "Social media yields high impressions but low immediate purchase intent because users are in a leisure/socializing mindset.",
            "Google search traffic converts at a much higher rate because users have already formed specific buying intent (e.g. searching 'best tacos in Miramar').",
            "On search engines, restaurants do not need to create demand; they only need to capture existing high-intent demand by ranking at the top."
        ],
        "numbers": [],
        "method": [
            "Prioritize local SEO ranking for high-intent cuisine + geo keywords before scaling broad social media awareness campaigns."
        ],
        "context": [
            "General consumer psychological framework comparing active search vs passive feed browsing."
        ]
    },
    {
        "serial": "009",
        "video_id": "IjWpMFaSXwQ",
        "title": "Best restaurant homepage setup for conversion",
        "category": "marketing",
        "file_name": "restaurant-homepage-structure.md",
        "tags": ["website-design", "conversion-rate", "menu-preview", "visual-marketing"],
        "key_info": [
            "Diners make fast visual decisions ('eating with their eyes') when visiting a restaurant website.",
            "The top section must communicate unique differentiation and story alongside an enticing food photo.",
            "The immediate follow-up section should display a curated slider of best-selling menu items with names and images to drive visitors directly into the menu."
        ],
        "numbers": [],
        "method": [
            "Structure the homepage in 2 key tiers:",
            "  1. Differentiation statement + brand story hint + flagship dish hero image.",
            "  2. Horizontal carousel/slider of top popular dishes prompting click-throughs into online ordering."
        ],
        "context": [
            "Website UX design principles based on conversion testing across independent restaurant websites."
        ]
    },
    {
        "serial": "010",
        "video_id": "Cs-zg-JR1_U",
        "title": "How to use restaurant reviews to increase sales",
        "category": "marketing",
        "file_name": "homepage-customer-reviews-seo.md",
        "tags": ["reviews", "social-proof", "seo-rankings", "conversion"],
        "key_info": [
            "Embedding customer reviews directly on the restaurant homepage provides critical social proof that accelerates dining decisions.",
            "Google algorithms use behavioral signals (dwell time, direct ordering clicks) from review engagement to rank websites higher.",
            "Hosting reviews on-site keeps visitors from leaving to third-party review platforms where negative reviews and competitors can divert them."
        ],
        "numbers": [
            "70% of potential guests check online customer reviews when deciding on a restaurant."
        ],
        "method": [
            "Feature curated high-rating customer reviews on the website homepage to satisfy diner validation without sending them to third-party aggregator sites."
        ],
        "context": [
            "Consumer behavior research regarding restaurant selection and Google ranking signals."
        ]
    },
    {
        "serial": "011",
        "video_id": "5aZfOA2rH0U",
        "title": "How to use your restaurant website to build your email list",
        "category": "marketing",
        "file_name": "website-vip-club-lead-capture.md",
        "tags": ["email-marketing", "lead-capture", "vip-club", "conversion"],
        "key_info": [
            "The vast majority of first-time restaurant website visitors browse and leave without placing an order.",
            "A prominent top banner capturing visitor contact information allows restaurants to market to visitors who would otherwise be lost.",
            "A 'VIP Club' framing creates perceived exclusivity and motivates visitors to share email, phone number, and birthday."
        ],
        "numbers": [
            "80% of restaurant website visitors do not place an order on their first visit."
        ],
        "method": [
            "Place a persistent top-of-page banner inviting visitors to join a VIP Club for exclusive specials, discounts, and event alerts."
        ],
        "context": [
            "Lead generation strategy utilized by Talking Tacos."
        ]
    },
    {
        "serial": "012",
        "video_id": "6fxwUcSfwzo",
        "title": "The #1 key to succeeding in restaurants",
        "category": "operations",
        "file_name": "hospitality-mindset-operations.md",
        "tags": ["hospitality", "customer-service", "operations", "culture"],
        "key_info": [
            "Restaurant success is fundamentally driven by genuine hospitality rather than food alone.",
            "Guests forgive minor food or timing flaws if the service culture makes them feel genuinely welcomed, remembered, and valued.",
            "Training front-of-house staff to treat every diner like family is the primary differentiator between struggling restaurants and beloved community institutions."
        ],
        "numbers": [],
        "method": [
            "Instill a hospitality-first culture where team members prioritize guest recognition, warmth, and proactive problem resolution."
        ],
        "context": [
            "Operational philosophy shared by veteran independent restaurant operators."
        ]
    },
    {
        "serial": "013",
        "video_id": "nLZ4oVJbI3g",
        "title": "Best restaurant website structure for conversion",
        "category": "marketing",
        "file_name": "restaurant-website-conversion-flow.md",
        "tags": ["website-design", "conversion-rate", "ux", "online-ordering"],
        "key_info": [
            "A high-converting restaurant website must guide visitors along a frictionless path to ordering.",
            "Websites that clutter visitors with PDF downloads, complex menus, or obscure navigation lose orders to third-party delivery apps.",
            "Clear call-to-action buttons for 'Order Online' must remain visible and accessible from every section of the site."
        ],
        "numbers": [],
        "method": [
            "Design the site hierarchy around three focal points: instant visual food appeal, fast crawlable text menus, and persistent one-click direct ordering buttons."
        ],
        "context": [
            "Conversion optimization benchmarks for independent restaurant websites."
        ]
    },
    {
        "serial": "014",
        "video_id": "G1ne-i_8uQI",
        "title": "The Alarming Reason Why Restaurants FAIL (Menu Market Fit)",
        "category": "menu",
        "file_name": "menu-market-fit-search-volume.md",
        "tags": ["menu-market-fit", "demand-validation", "search-volume", "concept-planning"],
        "key_info": [
            "A primary cause of restaurant failure is opening without 'Menu Market Fit'—offering food concepts that have insufficient local demand.",
            "Local demand can be validated for free before opening using Google Keyword Planner to check city-specific search volumes.",
            "Checking search volumes for cuisine types and core dishes reveals whether an unmet market need actually exists."
        ],
        "numbers": [
            "Benchmark: Over 500 searches per month in a specific city for a cuisine type indicates healthy, unmet consumer demand."
        ],
        "method": [
            "Open Google Keyword Planner, input core concept keywords (e.g. 'Italian restaurant', 'pasta', 'pizza'), select the target municipality, and verify search volume exceeds 500 monthly queries."
        ],
        "context": [
            "Pre-opening market validation strategy for prospective restaurant owners."
        ]
    },
    {
        "serial": "015",
        "video_id": "AGD5pa89EZI",
        "title": "How The Best Restaurants Do Branding",
        "category": "marketing",
        "file_name": "target-customer-brand-positioning.md",
        "tags": ["branding", "target-audience", "customer-personas", "positioning"],
        "key_info": [
            "Effective restaurant branding starts with identifying the ideal customer profile and their worldview rather than choosing logos and colors.",
            "Whether targeting comfort-seeking families or health-conscious trendsetters, all operational touchpoints must align.",
            "Consistent branding creates a distinct mental positioning so consumers instinctively think of the restaurant for a specific dining use-case."
        ],
        "numbers": [],
        "method": [
            "Define the target customer's lifestyle, values, and dining motivations first; align dining room aesthetics, menu language, social imagery, and website tone with that single identity."
        ],
        "context": [
            "Brand strategy analysis across high-growth independent restaurant concepts."
        ]
    },
    {
        "serial": "016",
        "video_id": "Tj8L1wacpLA",
        "title": "The Secret That The Top Restaurant Owners Have In Common (Hint: People)",
        "category": "labour",
        "file_name": "restaurant-staff-recruiting-strategy.md",
        "tags": ["recruiting", "staffing", "retention", "leadership"],
        "key_info": [
            "Top-performing restaurant owners act as 'Recruiter in Chief', viewing team building as their most essential operational duty.",
            "Paying baseline wages is table stakes; high-retention restaurants attract talent by offering skill building, mentorship, and community connection.",
            "Recruiting ambitious young workers (part-time students transitioning to full-time) working directly alongside the founder creates strong operational alignment."
        ],
        "numbers": [],
        "method": [
            "Run proactive outbound recruiting machines rather than relying solely on passive inbound help-wanted ads."
        ],
        "context": [
            "Management philosophy observed among top tech and restaurant entrepreneurs."
        ]
    },
    {
        "serial": "017",
        "video_id": "B6UP6RjnN80",
        "title": "5 things restaurants need to automate their marketing",
        "category": "marketing",
        "file_name": "automated-marketing-data-collection.md",
        "tags": ["marketing-automation", "sms-marketing", "email-marketing", "data-collection"],
        "key_info": [
            "80% of website traffic leaves without buying; automated marketing recovers revenue from this non-converting majority.",
            "To build an effective automated marketing engine, a restaurant must capture five key data assets from visitors:",
            "  1. Customer name",
            "  2. Email address",
            "  3. Mobile phone number (for SMS marketing)",
            "  4. Birthday (for birthday promotion automation)",
            "  5. Explicit marketing consent",
            "An irresistible upfront VIP offer is needed to incentivize opt-ins."
        ],
        "numbers": [
            "80% of website visitors bounce without ordering."
        ],
        "method": [
            "Deploy an opt-in lead capture banner collecting name, email, phone, birthday, and consent to feed automated drip sequences."
        ],
        "context": [
            "Marketing automation infrastructure implemented at Talking Tacos."
        ]
    },
    {
        "serial": "018",
        "video_id": "Pc5EJ7PdtD4",
        "title": "Why you need to be using this restaurant marketing strategy in 2023",
        "category": "marketing",
        "file_name": "founder-story-conversion-lift.md",
        "tags": ["storytelling", "average-check", "order-frequency", "website-conversion"],
        "key_info": [
            "Highlighting the authentic founding story of a local restaurant is a major competitive advantage over faceless corporate chains.",
            "Consumers actively prefer supporting people and families in their local community when they feel an emotional connection.",
            "A/B testing confirms that displaying the restaurant's story increases guest frequency, average check size, and online visitor-to-order conversion."
        ],
        "numbers": [],
        "method": [
            "Feature an authentic story summary on the homepage linked to a dedicated 'Our Story' page detailing the founders' background and culinary vision."
        ],
        "context": [
            "A/B test findings comparing restaurant sites with vs without founder story sections."
        ]
    },
    {
        "serial": "019",
        "video_id": "Ip3ZQh8YX9I",
        "title": "How to advertise your restaurant on Google for free",
        "category": "marketing",
        "file_name": "item-specific-seo-landing-pages.md",
        "tags": ["seo", "organic-traffic", "landing-pages", "menu-items"],
        "key_info": [
            "Every popular signature dish on a menu has dozens of local searchers seeking it monthly on Google.",
            "Creating dedicated website landing pages for individual popular menu items allows restaurants to rank organically for dish-level queries without paid Google Ads.",
            "Dedicated item pages should include dish descriptions, photos, and dish-specific customer reviews."
        ],
        "numbers": [
            "45 new customers generated every month organically from Google search rankings for specific dish landing pages (e.g., 'best garlic bread in Lakeside California')."
        ],
        "method": [
            "Publish standalone landing pages for top menu items with optimized descriptions, reviews, and images to capture organic dish-level searches."
        ],
        "context": [
            "Case data from Ottavio's Italian Restaurant in Lakeside, California."
        ]
    },
    {
        "serial": "020",
        "video_id": "2HHcPouMbZo",
        "title": "3 things every successful restaurant has on their website",
        "category": "marketing",
        "file_name": "above-the-fold-homepage-elements.md",
        "tags": ["website-design", "above-the-fold", "social-proof", "conversion"],
        "key_info": [
            "The 'above the fold' area (visible before scrolling) dominates user attention; most visitors never scroll down.",
            "To maximize conversion, top restaurant websites place three elements above the fold:",
            "  1. A clear hook statement sharing unique positioning and founding story.",
            "  2. A mouthwatering photograph of the restaurant's most popular signature dish.",
            "  3. Social proof (high star rating, review score, or recent order count)."
        ],
        "numbers": [
            "80% of a website visitor's viewing time is spent above the fold before scrolling."
        ],
        "method": [
            "Position the value proposition hook, flagship hero dish image, and live review/order social proof badges above the fold."
        ],
        "context": [
            "Website usability principles applied to restaurant digital ordering storefronts."
        ]
    },
    {
        "serial": "021",
        "video_id": "X5CU7Kt8MWg",
        "title": "Why every restaurant owner needs to know this psychology trick to increase sales",
        "category": "menu",
        "file_name": "menu-anchor-pricing-psychology.md",
        "tags": ["anchor-pricing", "menu-psychology", "average-check", "pricing"],
        "key_info": [
            "Diners do not evaluate prices in isolation; they evaluate prices relative to surrounding anchor prices on the menu.",
            "Placing a premium, high-priced item at the top of a menu section establishes a high psychological anchor.",
            "This makes standard high-margin dishes appear reasonably priced and affordable by comparison, driving higher check averages."
        ],
        "numbers": [],
        "method": [
            "Position an expensive specialty item at the head of each menu category to anchor consumer price perception and lift uptake of medium-priced, high-margin core dishes."
        ],
        "context": [
            "Behavioral economics and menu engineering principles applied to restaurant dining."
        ]
    },
    {
        "serial": "022",
        "video_id": "aj7Km6eSSGg",
        "title": "How this one email is saving restaurants owners $1,000s in delivery fees",
        "category": "delivery",
        "file_name": "delivery-migration-email-campaign.md",
        "tags": ["delivery-fees", "third-party-apps", "email-marketing", "direct-ordering"],
        "key_info": [
            "Restaurants lose thousands of dollars each month paying 20-30% commissions on third-party delivery marketplaces like DoorDash and Uber Eats.",
            "A single targeted customer email can successfully migrate delivery customers from third-party apps to direct ordering.",
            "The email educates loyal diners that ordering direct supports local restaurant survival while offering them lower prices or direct reward points."
        ],
        "numbers": [
            "Thousands of dollars in monthly marketplace commission fees saved by converting marketplace diners to direct channels."
        ],
        "method": [
            "Send an automated email explaining the impact of marketplace commissions and offering a first-order incentive on the restaurant's direct ordering site."
        ],
        "context": [
            "Direct channel migration strategy utilized by independent restaurant operators."
        ]
    },
    {
        "serial": "023",
        "video_id": "K6ETH3n9FQY",
        "title": "How restaurant owners are fighting back against bad Yelp reviews",
        "category": "customers",
        "file_name": "post-order-feedback-loop.md",
        "tags": ["reviews", "customer-feedback", "reputation-management", "yelp"],
        "key_info": [
            "An automated post-order feedback email asks guests for input immediately after receiving their meal.",
            "This strategy routes satisfied guests directly to public review platforms (Google, Yelp) to post 5-star ratings.",
            "Crucially, it intercepts dissatisfied customers before they post publicly, allowing management to resolve grievances privately."
        ],
        "numbers": [
            "70% of potential guests check online customer reviews before deciding to try a restaurant (data from GrowthHub)."
        ],
        "method": [
            "Trigger an automated feedback request email following each online order; direct positive responses to Google/Yelp and funnel negative feedback to an internal resolution form."
        ],
        "context": [
            "Reputation management system implemented by Antoinette at Ottavio's in California."
        ]
    },
    {
        "serial": "024",
        "video_id": "fq1heZlL9uQ",
        "title": "How one restaurant successfully used this email to drive an extra $2,000 a month",
        "category": "marketing",
        "file_name": "weekly-specials-email-broadcast.md",
        "tags": ["email-marketing", "sms-marketing", "weekly-specials", "sales-lift"],
        "key_info": [
            "Sending a weekly broadcast email and SMS showcasing a limited-time 'Special of the Week' generates predictable sales surges.",
            "High-quality food photography and vivid sensory descriptions trigger immediate visual appetite and ordering impulses.",
            "Promoting availability across dine-in, takeout, and app delivery captures guests across all channels."
        ],
        "numbers": [
            "Minimum of $500 in additional sales generated every week (over $2,000/month in incremental revenue)."
        ],
        "method": [
            "Send a weekly multi-channel broadcast (email + SMS) featuring a high-margin specialty dish with sensory descriptions and direct ordering links while ingredients last."
        ],
        "context": [
            "Results from Timmarie Shibley at Doo-Dah Diner in Wichita, Kansas, featuring their crab cake Benedict."
        ]
    },
    {
        "serial": "025",
        "video_id": "TyV8et5dTMA",
        "title": "Does your restaurant know this trick to build customer loyalty?",
        "category": "customers",
        "file_name": "authentic-owner-storytelling.md",
        "tags": ["customer-loyalty", "brand-connection", "founder-story", "word-of-mouth"],
        "key_info": [
            "Authentic personal stories (family heritage, immigration, passion for culinary craft) build deep emotional connections with diners.",
            "Customers strongly prefer buying from individuals they know and respect in their local communities over national corporate chains.",
            "Diners who know the story and owner behind a restaurant order more frequently, exhibit higher lifetime loyalty, and generate more word-of-mouth referrals."
        ],
        "numbers": [],
        "method": [
            "Communicate the founder's authentic journey across menus, packaging, website, and social channels to build community loyalty."
        ],
        "context": [
            "Observed marketing pattern among top-performing independent restaurant owners."
        ]
    },
    {
        "serial": "026",
        "video_id": "gF7W-huC_48",
        "title": "The Hangover Special that made this restaurant owner record profits",
        "category": "promotions",
        "file_name": "new-years-hangover-special.md",
        "tags": ["holiday-promotions", "new-years-day", "low-food-cost", "takeout-records"],
        "key_info": [
            "New Year's Day is the second busiest day of the year for restaurant takeout, yet many independent operators remain closed.",
            "Re-positioning comforting, broth-based dishes (like Vietnamese pho) as a 'Hangover Special' taps into massive holiday takeout demand.",
            "Offering a free hangover item conditional on a spending threshold drives check sizes while maintaining healthy margins due to low food costs."
        ],
        "numbers": [
            "A day previously generating $0 became the single best-performing sales day of the entire year.",
            "Orders above a $50 minimum threshold received a free hangover pho bowl."
        ],
        "method": [
            "Open on high-demand takeout holidays with themed specialty promotions and a $50+ order minimum threshold tied to a low-food-cost giveaway."
        ],
        "context": [
            "Case study from Sandy, owner of Cyclo Noodles in Long Beach, California."
        ]
    },
    {
        "serial": "027",
        "video_id": "aU-jhWgIPto",
        "title": "Why every restaurant should use THIS menu hack from Domino's pizza to avoid decision fatigue",
        "category": "menu",
        "file_name": "step-by-step-menu-decision-fatigue.md",
        "tags": ["decision-fatigue", "menu-engineering", "ordering-flow", "conversion"],
        "key_info": [
            "Decision fatigue occurs when customers are presented with excessive options simultaneously, leading to overwhelm and abandoned orders.",
            "Domino's combats decision fatigue by structuring their digital ordering experience sequentially rather than presenting the entire menu upfront.",
            "Initial screens present only 3 curated combo offers; clicking into the menu reveals one category at a time starting with highest-priority pizzas."
        ],
        "numbers": [
            "3 combo deal options displayed initially to prevent choice paralysis."
        ],
        "method": [
            "Break online menu ordering into sequential steps: show 3 top bundle/combo options first, followed by category-by-category navigation."
        ],
        "context": [
            "Digital ordering UI/UX strategy analyzed from Domino's Pizza web and app platforms."
        ]
    },
    {
        "serial": "028",
        "video_id": "fXde7SFiWpU",
        "title": "How this restaurant is getting a 1250% return with this marketing strategy",
        "category": "marketing",
        "file_name": "new-mover-direct-mail-roi.md",
        "tags": ["direct-mail", "roi", "customer-acquisition", "new-movers"],
        "key_info": [
            "Direct mail targeting newly relocated families produces exceptional marketing ROI for local restaurants.",
            "New residents have higher average household spending, larger family dining checks, and no entrenched loyalty to local competitors.",
            "A personalized welcoming letter paired with a free pizza incentive captures new movers before competitors reach them."
        ],
        "numbers": [
            "$2,700+ per month in additional revenue generated from less than $200 in monthly marketing spend (1,250% marketing ROI)."
        ],
        "method": [
            "Partner with a direct mail data provider to target new residential move-ins within local zip codes, sending a personalized welcome letter with a free core item coupon."
        ],
        "context": [
            "Case data from Scott Anthony, owner of Punxsy Pizza in Punxsutawney, Pennsylvania."
        ]
    },
    {
        "serial": "029",
        "video_id": "vxaZMu9itHk",
        "title": "The genius reason behind this restaurant marketing strategy will surprise you",
        "category": "promotions",
        "file_name": "super-bowl-free-delivery-economics.md",
        "tags": ["free-delivery", "event-marketing", "average-check", "super-bowl"],
        "key_info": [
            "Super Bowl Sunday is one of the heaviest restaurant delivery days of the year, driven by group and family gatherings.",
            "Offering free delivery costs the restaurant $3–$5 per order, but generates huge returns when customer order sizes are large.",
            "Group watch parties lift average delivery check sizes well over $150, making absorbing nominal delivery costs highly accretive to net profit."
        ],
        "numbers": [
            "Average delivery check size exceeds $150 on Super Bowl Sunday.",
            "Delivery fee cost to restaurant: several dollars ($3–$5) per order."
        ],
        "method": [
            "Offer free delivery on major group-viewing sporting events where high check sizes dilute delivery delivery expenses and boost gross margin dollars."
        ],
        "context": [
            "Operational strategy from Sean, owner of Upper Crust Pizzeria in Beverly Hills and Culver City, California."
        ]
    },
    {
        "serial": "030",
        "video_id": "iK4wPvUI8bA",
        "title": "The 2009 'Cardboard Pizza' commercial from Domino's that turned around their entire company",
        "category": "marketing",
        "file_name": "radical-transparency-advertising.md",
        "tags": ["transparency", "brand-turnaround", "advertising", "customer-feedback"],
        "key_info": [
            "Radical transparency in advertising can reverse declining brand sentiment when operational quality is meaningfully upgraded.",
            "Domino's 2009 turnaround campaign publicly broadcast negative customer focus group comments ('tastes like cardboard') alongside chef commitments to reformulate.",
            "Demonstrating vulnerability and incorporating customer feedback builds credibility that generic promotional claims cannot achieve."
        ],
        "numbers": [],
        "method": [
            "Address customer critiques directly, publicize recipe and operational improvements, and invite diners to test the upgraded offering."
        ],
        "context": [
            "Analysis of Domino's Pizza 2009 brand relaunch campaign."
        ]
    },
    {
        "serial": "031",
        "video_id": "wjPfIAHyiO0",
        "title": "Why direct mail marketing for restaurants is not dead in 2023",
        "category": "marketing",
        "file_name": "direct-mail-deliverability-and-standout.md",
        "tags": ["direct-mail", "marketing-channels", "attention", "retention"],
        "key_info": [
            "Physical mailboxes have far less marketing clutter today than digital inboxes, creating higher open and notice rates.",
            "A tangible, well-crafted letter or postcard remains in the home (on the refrigerator or counter) for days, serving as persistent physical advertising.",
            "Direct mail is particularly effective for neighborhood businesses targeting home owners and new families."
        ],
        "numbers": [],
        "method": [
            "Combine physical direct mail for new neighborhood customer acquisition with digital SMS/email channels for subsequent retention."
        ],
        "context": [
            "Marketing channel effectiveness comparison in local restaurant acquisition."
        ]
    },
    {
        "serial": "032",
        "video_id": "crdBrmFGhDU",
        "title": "How gamifying your loyalty program like Domino's is a win-win for your restaurant and your customers",
        "category": "customers",
        "file_name": "gamified-loyalty-rewards.md",
        "tags": ["loyalty-programs", "gamification", "repeat-frequency", "rewards"],
        "key_info": [
            "Traditional punch cards and static point systems fail to sustain long-term engagement.",
            "Gamifying rewards (progress bars, unlocking milestones, tiered perks) stimulates psychological desire for goal completion.",
            "Domino's Piece of the Pie rewards visualizes progress toward free pizza, driving repeat ordering cadence."
        ],
        "numbers": [],
        "method": [
            "Implement a visual progress-based rewards system that clearly displays how close the customer is to unlocking their next reward."
        ],
        "context": [
            "Loyalty gamification mechanics based on enterprise restaurant mobile applications."
        ]
    },
    {
        "serial": "033",
        "video_id": "1PKSKqu975s",
        "title": "This is the perfect time to send direct mail as a restaurant if you want more regular customers",
        "category": "marketing",
        "file_name": "new-resident-direct-mail-timing.md",
        "tags": ["direct-mail", "timing", "new-residents", "lead-filtering"],
        "key_info": [
            "Timing is everything in new-mover direct mail marketing: mailings must arrive during the initial habit-forming window.",
            "Letters arriving less than three weeks after move-in reach families before they establish dining routines or choose competitor restaurants.",
            "Filtering out local address changers ensures marketing dollars target true newcomers without existing brand loyalties."
        ],
        "numbers": [
            "$2,700+ monthly revenue generated on under $200 in monthly spend.",
            "Delivery timing window: less than 3 weeks post-move-in."
        ],
        "method": [
            "Pull monthly new-mover lists, filter for out-of-area zip code arrivals, and trigger personalized letters arriving within 21 days of relocation."
        ],
        "context": [
            "Operational direct mail execution details from Punxsy Pizza in Pennsylvania using Moving Targets."
        ]
    },
    {
        "serial": "034",
        "video_id": "ymk3qCmTQCY",
        "title": "The interesting reason why this restaurant owner donated a meal for every meal ordered",
        "category": "promotions",
        "file_name": "cause-marketing-low-food-cost.md",
        "tags": ["cause-marketing", "food-cost", "charity-promotions", "sustainability"],
        "key_info": [
            "Cause marketing promotions (e.g. donating one meal to feed the hungry for every order placed) build massive community goodwill and ordering spikes.",
            "To make one-for-one meal donation promotions financially sustainable, the donated dish must have very low food costs.",
            "Using nutrient-dense, calorie-rich plant or grain-based dishes keeps donation expenses negligible, whereas meat-heavy dishes destroy promotion profitability."
        ],
        "numbers": [
            "One meal donated per order received on designated holiday promotions."
        ],
        "method": [
            "Design one-for-one charitable promotions around high-nutrition, low-cost ingredients (beans, lentils, rice) to maintain financial sustainability."
        ],
        "context": [
            "Martin Luther King Jr. Day promotion by Raj at Itihaas Indian Restaurant in Birmingham."
        ]
    },
    {
        "serial": "035",
        "video_id": "X0S-i0nIwQo",
        "title": "Why every restaurant needs to know about this marketing hack from Domino's pizza",
        "category": "promotions",
        "file_name": "urgency-scarcity-limited-time-deals.md",
        "tags": ["scarcity", "urgency", "lto", "promotions", "fear-of-missing-out"],
        "key_info": [
            "Consumers delay purchasing when offers appear permanently available without urgency.",
            "Domino's maintains a dynamic 'Deals' section on its web and app interfaces that changes frequently, supported by email and text notifications.",
            "Limited-time offers (LTOs) and weekend-only specials generate fear of missing out (FOMO) that forces immediate ordering action."
        ],
        "numbers": [],
        "method": [
            "Rotate limited-time promotions on a dedicated web/app deals tab and broadcast expiration deadlines via email and SMS."
        ],
        "context": [
            "Promotional rotation strategy utilized by Domino's Pizza."
        ]
    },
    {
        "serial": "036",
        "video_id": "iPg_e6gpT8o",
        "title": "How one successful restaurant figured out how to give away free food profitably",
        "category": "food-cost",
        "file_name": "loss-leader-high-margin-cross-selling.md",
        "tags": ["food-cost", "loss-leader", "cross-selling", "acquisition-cost", "margins"],
        "key_info": [
            "Offering a free flagship food item acts as a profitable loss leader when customer acquisition cost is offset by cross-selling high-margin add-ons.",
            "Families claiming a free medium pizza rarely order the free item alone; they routinely purchase appetizers, beverages, and desserts.",
            "These high-margin companion items have very low food costs, making the overall initial transaction highly profitable."
        ],
        "numbers": [
            "Free medium pizza with unlimited toppings menu price: $17.",
            "Food cost percentage on pizza: 30% (actual cost to restaurant: $5.10).",
            "Total customer acquisition cost including direct mail: $13.33.",
            "Average first-transaction ticket: well over $40 (driven by appetizers, drinks, and desserts with low food cost and high gross margin).",
            "Monthly revenue lift: over $2,700 on less than $200 ad spend."
        ],
        "method": [
            "Calculate total cost of acquisition (mail cost + COGS of free item) and ensure ordering pathways actively prompt for high-margin add-ons (drinks, sides, desserts)."
        ],
        "context": [
            "Financial breakdown from Punxsy Pizza in Punxsutawney, Pennsylvania."
        ]
    },
    {
        "serial": "037",
        "video_id": "uXYS2URNJ4Y",
        "title": "How this marketing strategy can get you to do something without even realizing it",
        "category": "customers",
        "file_name": "reciprocity-in-restaurant-gifting.md",
        "tags": ["reciprocity", "behavioral-psychology", "customer-spending", "loyalty"],
        "key_info": [
            "The psychological principle of reciprocity dictates that when an individual receives an unexpected gift or favor, they feel a compelling subconscious urge to give back.",
            "Classic behavioral research (Dennis, 1971) showed giving an unsolicited small soda more than doubled the recipient's subsequent willingness to purchase raffle tickets.",
            "In restaurants, offering small unexpected treats (churros, garlic knots, amuse-bouche) significantly increases customer spend, tips, and repeat visits."
        ],
        "numbers": [
            "Unsolicited gift increased subsequent compliance/purchase rate by more than double (>100% increase)."
        ],
        "method": [
            "Provide low-cost surprise-and-delight items to diners to trigger reciprocity, resulting in higher average checks and higher review propensity."
        ],
        "context": [
            "Behavioral psychology study applied to hospitality customer interaction."
        ]
    },
    {
        "serial": "038",
        "video_id": "uIauTUcTxAU",
        "title": "The 3 things every successful direct mail strategy for restaurants should have",
        "category": "marketing",
        "file_name": "direct-mail-core-components.md",
        "tags": ["direct-mail", "copywriting", "personalization", "offers"],
        "key_info": [
            "Successful restaurant direct mail campaigns combine three essential marketing components:",
            "  1. An irresistible offer centered around the word 'Free' (e.g. free medium pizza).",
            "  2. Personalization addressed directly to the recipient by name, personally signed by the owner rather than a corporate entity.",
            "  3. High-quality visual photography of signature dishes, acknowledging that diners 'eat with their eyes'."
        ],
        "numbers": [
            "$2,700+ monthly revenue generated from under $200 in monthly spend."
        ],
        "method": [
            "Format direct mail letters with personal recipient salutations, owner signatures, appetizing food photography, and clear free-item redemption instructions."
        ],
        "context": [
            "Proven campaign template from Punxsy Pizza in Pennsylvania."
        ]
    },
    {
        "serial": "039",
        "video_id": "PUa8H4S9d_w",
        "title": "Why This Fishy Restaurant Concept Is Booming In 2024",
        "category": "finance",
        "file_name": "poke-restaurant-unit-economics.md",
        "tags": ["unit-economics", "poke", "profit-margins", "fast-casual", "labor-costs"],
        "key_info": [
            "Poke restaurants present superior fast-casual unit economics due to small footprints, high ticket sizes, and fast customer throughput.",
            "Poke bowls require no heavy cooking equipment or ventilation hoods, keeping initial capital expenditure and space requirements low.",
            "Assembly-line preparation requires minimal kitchen labor (1–2 staff on shift), and counter service achieves 20-minute customer table turnover."
        ],
        "numbers": [
            "Average check size: consistently over $40.",
            "Operating profit margins: over 20%.",
            "Store footprint: under 1,000 square feet.",
            "Initial opening capital expenditure: under $200,000.",
            "Staffing requirements: 1 to 2 counter employees per shift.",
            "Customer turnover time: under 20 minutes from entry to exit."
        ],
        "method": [
            "Select high-foot-traffic micro-footprints (<1,000 sq ft) for no-cook assembly concepts (poke) to maximize revenue per square foot with 1–2 staff."
        ],
        "context": [
            "US fast casual concept economics and operating benchmarks."
        ]
    },
    {
        "serial": "040",
        "video_id": "lDTMg_A2EWY",
        "title": "Create Loyal Restaurant Customers With This One Simple Trick",
        "category": "customers",
        "file_name": "identity-based-community-loyalty.md",
        "tags": ["identity-marketing", "community-loyalty", "affinity-groups", "repeat-visits"],
        "key_info": [
            "Diners make purchasing choices that validate their personal identity and social affiliations.",
            "Recognizing and catering to specific local affinity groups (school parent communities, military, first responders, seniors) creates natural trust.",
            "Offering dedicated affinity discount codes gives customers VIP status, driving significantly higher ordering frequency than generic discounts."
        ],
        "numbers": [],
        "method": [
            "Create dedicated VIP codes and targeted recognition programs for distinct community identity groups to drive repeat purchase frequency."
        ],
        "context": [
            "Identity marketing principles applied to neighborhood independent restaurant operations."
        ]
    },
    {
        "serial": "041",
        "video_id": "bUktgMIMaKw",
        "title": "Find Top Restaurant Staff With This Simple Secret",
        "category": "labour",
        "file_name": "staff-recruitment-channels.md",
        "tags": ["recruiting", "staffing", "employee-retention", "culture"],
        "key_info": [
            "Top restaurant staff are rarely found by posting generic ads on job boards where disengaged workers apply en masse.",
            "High-performing operators build active talent pipelines by networking into local high schools, colleges, and community organizations.",
            "Offering clear skill development and business exposure attracts motivated workers seeking growth beyond basic hourly wages."
        ],
        "numbers": [],
        "method": [
            "Build direct relationships with local vocational programs, high school counselors, and university clubs to recruit ambitious talent."
        ],
        "context": [
            "Hospitality workforce management and recruitment techniques."
        ]
    },
    {
        "serial": "042",
        "video_id": "BIa1EpUPf1Y",
        "title": "Restaurants Should Steal This BOGO Strategy To Maximize Profit",
        "category": "promotions",
        "file_name": "bogo-low-food-cost-threshold.md",
        "tags": ["bogo", "food-cost-percentage", "promotions", "margin-protection"],
        "key_info": [
            "Buy-One-Get-One (BOGO) promotions must be restricted strictly to menu items with food costs below 15%.",
            "When giving away a second item for free, the effective food cost doubles; starting from a 15% base ensures the order remains under the healthy 30% food cost ceiling.",
            "Running BOGO promotions on high-cost items (e.g. meat-based entrees at 30% food cost) spikes effective food costs to 60%, completely destroying profitability."
        ],
        "numbers": [
            "Maximum food cost threshold for BOGO promotions: under 15% of menu price.",
            "Healthy ceiling for total order food cost: under 30%.",
            "Disastrous food cost spike when BOGO is applied to 30% meat dish: 60% food cost."
        ],
        "method": [
            "Audit item recipe costs; designate only items with <15% COGS (garlic bread, churros, sodas, desserts) as eligible for BOGO promotions."
        ],
        "context": [
            "Financial formula and guardrail rule for promotional pricing in restaurants."
        ]
    },
    {
        "serial": "043",
        "video_id": "FUuE8nxYQgQ",
        "title": "Copy This Restaurant With INSANE Profit Margins",
        "category": "finance",
        "file_name": "artisan-ice-cream-unit-economics.md",
        "tags": ["unit-economics", "profit-margins", "ice-cream", "real-estate", "labor-efficiency"],
        "key_info": [
            "Artisan ice cream shops operate with exceptional profit margins due to high demand, low ingredient costs, minimal square footage, and low labor skill requirements.",
            "Stores require essentially two counter staff to operate, avoiding kitchen cook lines or complex culinary prep.",
            "Real estate occupancy costs are low because concepts require only a small footprint (~1,000 sq ft) housing display coolers and cup/cone storage."
        ],
        "numbers": [
            "Average American consumes roughly 20 lbs of ice cream per year.",
            "Over 80% of Americans eat ice cream multiple times per month.",
            "Revenue benchmark: over $1,000,000 per year per store (based on Salt & Straw model).",
            "Net profit margin: approximately 20%.",
            "Store footprint: approximately 1,000 square feet.",
            "Staffing requirements: 2 people at the counter per shift."
        ],
        "method": [
            "Differentiate through unique artisanal flavors and replicate high-volume, low-equipment micro-retail ice cream shop footprints in unsaturated markets."
        ],
        "context": [
            "Concept financial analysis of Salt & Straw (36 locations across the US)."
        ]
    },
    {
        "serial": "044",
        "video_id": "krMzKsCe18Y",
        "title": "The Simple Restaurant Hack To Increase The Average Check Size",
        "category": "menu",
        "file_name": "free-item-average-check-threshold.md",
        "tags": ["average-check", "spend-thresholds", "upselling", "food-cost"],
        "key_info": [
            "A structured spending threshold incentivizes diners to add items to their cart to qualify for a free gift.",
            "The free reward item must have a food cost below 10% of its menu price so the giveaway costs the operator very little.",
            "The spend threshold should be set strategically $5 to $10 higher than the restaurant's current average check size."
        ],
        "numbers": [
            "Target threshold increase: set spend goal $5 to $10 above baseline average check size.",
            "Food cost requirement on reward item: under 10% of menu price."
        ],
        "method": [
            "1. Calculate baseline average check size.",
            "2. Establish an order spending threshold $5–$10 above baseline.",
            "3. Select a popular menu item with <10% COGS as the giveaway.",
            "4. Configure digital ordering checkout prompts alerting guests how much more they must spend to unlock the free item."
        ],
        "context": [
            "Average check optimization technique applied across online ordering interfaces."
        ]
    },
    {
        "serial": "045",
        "video_id": "bBBWbU3wTbQ",
        "title": "Why You Should Open THIS Trending Restaurant Concept",
        "category": "food-cost",
        "file_name": "gourmet-ramen-economics.md",
        "tags": ["food-cost", "ramen", "inventory-management", "shelf-life", "average-check"],
        "key_info": [
            "Gourmet ramen concepts exhibit very low food costs combined with high check averages from group and family takeout orders.",
            "Core components are inexpensive (noodles, broth, seasonings, water), keeping blended food costs low even with specialty meats included.",
            "Noodles have an exceptionally long shelf life (fresh ramen stores for weeks), dramatically simplifying inventory management and minimizing spoilage.",
            "Ramen accommodates diverse diets (vegan, gluten-free, low-carb) while maintaining broad appeal for indulgent dining."
        ],
        "numbers": [
            "Blended food cost percentage: often under 10% across the board.",
            "Noodle shelf life: fresh noodles store for multiple weeks without spoiling."
        ],
        "method": [
            "Leverage high-margin noodle/broth dishes with extended shelf-life ingredients to eliminate food waste while capturing high average check sizes."
        ],
        "context": [
            "Fast-casual Japanese concept economics and menu operational analysis."
        ]
    },
    {
        "serial": "046",
        "video_id": "ClzPynBqAdo",
        "title": "$1,000,000+ Restaurant Idea With A Small Footprint",
        "category": "finance",
        "file_name": "health-cafe-unit-economics.md",
        "tags": ["unit-economics", "health-cafe", "revenue-per-sqft", "profit-margins"],
        "key_info": [
            "Health cafe concepts generate outstanding sales per square foot and profit margins due to affluent demographic appeal and all-day multi-daypart demand.",
            "Health food consumers exhibit lower price sensitivity and regularly pay premium prices for clean, functional food, coffee, and tea.",
            "The concept spans multiple meal occasions (breakfast, coffee, lunch, dinner), driving high table turns across the entire day."
        ],
        "numbers": [
            "Annual revenue: over $1,000,000.",
            "Net annual profit: over $300,000 (net margin of ~30%).",
            "Store footprint: 900 square feet.",
            "Average check size range: $27 on the low end to over $50 in affluent areas."
        ],
        "method": [
            "Operate small-footprint (<1,000 sq ft) health cafes offering all-day items (bowls, coffee, functional teas) in high-income neighborhoods."
        ],
        "context": [
            "Financial performance data from an expanding franchise health cafe concept in Los Angeles, California."
        ]
    },
    {
        "serial": "047",
        "video_id": "Ma31BsmLl8U",
        "title": "The Secret Formula Behind Restaurant Loyalty",
        "category": "customers",
        "file_name": "repeat-visit-loyalty-curve.md",
        "tags": ["loyalty-curve", "retention-rates", "customer-lifetime-value", "guest-experience"],
        "key_info": [
            "Customer retention follows an exponential probability curve based on repeat visits.",
            "A flawless initial visit still leaves more than half of guests unlikely to return; the retention rate increases slightly after a second visit.",
            "The third flawless visit is the critical inflection threshold where customer retention surges dramatically, turning a diner into a 'customer for life'."
        ],
        "numbers": [
            "Likelihood to return after 1st flawless experience: 40%.",
            "Likelihood to return after 2nd flawless experience: 42%.",
            "Likelihood to return after 3rd flawless experience: 70% (customer-for-life inflection point)."
        ],
        "method": [
            "Tag first-time and second-time guests in the POS/ordering system to deliver proactive VIP service, actively bridging diners to their crucial third visit."
        ],
        "context": [
            "Empirical customer retention statistics in restaurant dining and guest frequency modeling."
        ]
    },
    {
        "serial": "048",
        "video_id": "Pqnwh3p0YiE",
        "title": "The #1 Most Profitable Restaurant In 2024",
        "category": "food-cost",
        "file_name": "bubble-tea-cogs-and-margins.md",
        "tags": ["bubble-tea", "cogs", "food-cost", "shelf-life", "profit-margins"],
        "key_info": [
            "Bubble tea shops achieve among the highest gross margins in food service because their cost of goods sold (COGS) is a fraction of standard restaurants.",
            "The primary product consists of water, tea base, powders, syrups, and tapioca pearls—shelf-stable ingredients that rarely expire.",
            "Low waste and small physical space requirements drive outsized profitability compared to full-kitchen concepts."
        ],
        "numbers": [
            "Average Cost of Goods Sold (COGS): just 10% (compared to 30%+ in traditional restaurants).",
            "Gross margin per order: roughly 3x higher than standard restaurants on an equivalent sales dollar."
        ],
        "method": [
            "Utilize highly shelf-stable powdered/syrup ingredient supply chains to virtually eliminate food spoilage while operating out of micro-retail footprints."
        ],
        "context": [
            "Beverage retail sector economics and cost of goods benchmarking."
        ]
    },
    {
        "serial": "049",
        "video_id": "FgDmnLQSfJs",
        "title": "Only The Most Successful Restaurants Do THIS Discount",
        "category": "promotions",
        "file_name": "conditional-discount-app-adoption.md",
        "tags": ["conditional-discounts", "mobile-app", "customer-acquisition", "order-frequency"],
        "key_info": [
            "Unconditional price discounting devalues the brand and attracts low-margin bargain hunters who never return.",
            "Top restaurant enterprises utilize 'conditional discounts'—granting a percentage off only when the customer performs a high-value behavior.",
            "Conditioning discounts on downloading the branded app or placing a direct online order permanently lifts long-term order frequency."
        ],
        "numbers": [],
        "method": [
            "Condition discounts on actions that produce long-term customer lifetime value (e.g., 'Get 20% off your first order on our mobile app')."
        ],
        "context": [
            "Promotional architecture analyzed from enterprise chains including Chick-fil-A and Chipotle."
        ]
    },
    {
        "serial": "050",
        "video_id": "DgrsDG9MdWw",
        "title": "Sushi Restaurants Use THIS Hack To Make More Profit",
        "category": "menu",
        "file_name": "menu-naming-perceived-value.md",
        "tags": ["menu-engineering", "perceived-value", "pricing-power", "menu-naming"],
        "key_info": [
            "Naming menu items descriptively around locations, experiences, or evocative themes shifts customer perception away from commodity ingredient costs.",
            "In sushi restaurants, a generic 'Salmon Roll' priced at $9 can be rebranded as a 'Philadelphia Roll' (with minimal added cream cheese) and sold for $15.",
            "Diners gladly pay premium prices for perceived experiential branding, generating pure gross profit margin lift."
        ],
        "numbers": [
            "Salmon roll price: $9.",
            "Philadelphia roll price: $15 (an incremental $6 price premium per item with negligible ingredient cost difference)."
        ],
        "method": [
            "Replace generic ingredient-based menu names with creative geographic or experiential titles to elevate perceived value and capture premium margins."
        ],
        "context": [
            "Menu pricing and psychology techniques observed in contemporary sushi restaurants."
        ]
    }
]


def format_markdown(entry):
    lines = []
    lines.append("---")
    lines.append(f'serial: "{entry["serial"]}"')
    lines.append(f'title: {entry["title"]}')
    lines.append("source: YouTube")
    lines.append(f'category: {entry["category"]}')
    lines.append(f'tags: [{", ".join(entry["tags"])}]')
    lines.append("---")
    lines.append("")
    lines.append("# Key Information")
    lines.append("")
    for k in entry["key_info"]:
        if k.startswith("  - "):
            lines.append(k)
        else:
            lines.append(f"- {k}")
    lines.append("")

    if entry.get("numbers"):
        lines.append("# Numbers / Calculations")
        lines.append("")
        for n in entry["numbers"]:
            lines.append(f"- {n}")
        lines.append("")

    if entry.get("method"):
        lines.append("# Useful Method / Takeaway")
        lines.append("")
        for m in entry["method"]:
            if m.startswith("  "):
                lines.append(m)
            else:
                lines.append(f"- {m}")
        lines.append("")

    if entry.get("context"):
        lines.append("# Context")
        lines.append("")
        for c in entry["context"]:
            lines.append(f"- {c}")
        lines.append("")

    # Mandatory final section
    lines.append("# Source")
    lines.append("")
    lines.append(f"Video: https://www.youtube.com/shorts/{entry['video_id']}")
    lines.append("")

    return "\n".join(lines)


def main():
    processed_serials = set()

    for item in ENTRIES:
        cat_dir = os.path.join("knowledge", item["category"])
        os.makedirs(cat_dir, exist_ok=True)
        file_path = os.path.join(cat_dir, item["file_name"])

        content = format_markdown(item)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        processed_serials.add(int(item["serial"]))
        print(f"[{item['serial']}/050] Saved: {file_path}")

    # Update CSV to mark processed = yes for serials 1 to 50
    csv_path = os.path.join("sources", "youtube-lists", "ownercom-shorts.csv")
    rows = []
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                s_int = int(row["serial"])
                if s_int in processed_serials:
                    row["processed"] = "yes"
                rows.append(row)

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    print(f"\nSuccessfully processed and saved all 50 entries.")
    print(f"Updated {csv_path}: marked serials 001-050 as processed: yes.")


if __name__ == "__main__":
    main()
