"""
Competitor / product reference engine.

Phase 1 (current): returns realistic *mock* reference data for a (category,
target_market, channel, price_tier) combination. The structure mirrors what
a real source-of-truth would look like, so the agents and prompts can consume
it today and switch to live data later.

Phase 2 (future): wire live sources behind the same interface — supermarket
APIs (e.g. Edeka/REWE catalogues), Amazon Product Advertising API, Rakuten
Ichiba, Olive Young, Coupang, Yahoo! Japan Shopping, distributor PDFs,
retail trend reports.

TODO (live data):
    - Plug a search adapter behind `get_competitor_references` that fans
      out to retail/marketplace APIs filtered by (category, market, channel).
    - Cache by (category, market, channel, price_tier) — competitor patterns
      change on the weeks/months timescale, not seconds.
    - Add a `freshness_days` field to each CompetitorReference so the agents
      can de-weight stale signals.

This module is intentionally provider-agnostic so the agent layer never
needs to know whether the data is live or mock.
"""

from __future__ import annotations
from typing import List, TypedDict, Literal


# ----------------------------------------------------------------------------
# Types — mirror the TS interfaces in the product brief.
# ----------------------------------------------------------------------------

PriceTier = Literal['budget', 'mainstream', 'premium', 'luxury']

SourceType = Literal[
    'supermarket',
    'pharmacy',
    'convenience_store',
    'health_store',
    'specialty_store',
    'amazon',
    'local_ecommerce',
    'distributor_catalogue',
    'brand_website',
    'trend_report',
]


class CompetitorReference(TypedDict, total=False):
    brandName: str
    productName: str
    category: str
    market: str
    channel: str
    priceTier: PriceTier
    visibleClaims: List[str]
    trustMarkers: List[str]
    colorPalette: List[str]
    packagingStyle: str
    hierarchyPattern: List[str]
    typographyStyle: str
    imageryStyle: str
    sustainabilitySignals: List[str]
    originSignals: List[str]
    functionalSignals: List[str]
    emotionalSignals: List[str]
    riskNotes: List[str]
    sourceType: SourceType


class CommonPatterns(TypedDict, total=False):
    claims: List[str]
    colors: List[str]
    trustMarkers: List[str]
    hierarchy: List[str]
    packagingStyles: List[str]
    typography: List[str]
    imagery: List[str]
    priceSignals: List[str]


class MarketReferenceSummary(TypedDict, total=False):
    targetMarket: str
    category: str
    channel: str
    referenceProducts: List[CompetitorReference]
    commonPatterns: CommonPatterns
    whiteSpaceOpportunities: List[str]
    overusedPatterns: List[str]
    adaptationImplications: List[str]
    source: str  # 'mock' for now; 'live' or specific provider name later.


# ----------------------------------------------------------------------------
# Channel prioritization rules.
# ----------------------------------------------------------------------------

_SUPPLEMENT_CATEGORIES = {'Supplement'}
_FOOD_BEV_CATEGORIES = {'Food', 'Beverage'}


def _priority_channels_for_category(category: str, requested_channel: str) -> List[str]:
    """
    Which reference channels to pull for the category.
    The requested channel always ranks first; the rest are category defaults.
    """
    category = (category or '').strip()
    if category in _SUPPLEMENT_CATEGORIES:
        defaults = ['pharmacy', 'health_store', 'amazon', 'specialty_store', 'brand_website']
    elif category in _FOOD_BEV_CATEGORIES:
        defaults = ['supermarket', 'convenience_store', 'local_ecommerce', 'specialty_store']
    else:  # Private Label and others
        defaults = ['supermarket', 'distributor_catalogue', 'amazon', 'local_ecommerce']

    if requested_channel and requested_channel in defaults:
        defaults.remove(requested_channel)
    if requested_channel:
        defaults.insert(0, requested_channel)
    return defaults


# ----------------------------------------------------------------------------
# Mock datasets.
# Keys are (category, target_market). Lookups try (cat, market) → falls back
# to a generic category-level set.
# ----------------------------------------------------------------------------

_MOCK_REFERENCES: dict = {
    # ============== 1) Supplement entering Japan ==============
    ('Supplement', 'Japan'): {
        'referenceProducts': [
            {
                'brandName': 'DHC',
                'productName': 'DHC Vitamin C 60-day',
                'category': 'Supplement',
                'market': 'Japan',
                'channel': 'pharmacy',
                'priceTier': 'mainstream',
                'visibleClaims': ['60日分', '1000mg per day', 'Made in Japan'],
                'trustMarkers': ['GMP-grade manufacturing', 'JAS-style seal', 'Daily-dose clarity'],
                'colorPalette': ['#FFFFFF', '#1A1A1A', '#D6A85B'],
                'packagingStyle': 'Compact pouch / blister stick with restrained typography',
                'hierarchyPattern': [
                    'Quantified daily dose', 'Active ingredient + mg',
                    'Brand mark', 'Day-supply count', 'Regulatory line',
                ],
                'typographyStyle': 'Conservative gothic + Mincho serif for legal',
                'imageryStyle': 'No lifestyle imagery — pure typographic',
                'sustainabilitySignals': [],
                'originSignals': ['Made in Japan'],
                'functionalSignals': ['Specific mg amount', 'Day-supply countdown'],
                'emotionalSignals': [],
                'riskNotes': ['Health claims are conservative; PMDA-aligned wording.'],
                'sourceType': 'pharmacy',
            },
            {
                'brandName': 'FANCL',
                'productName': 'FANCL Mild Cleansing Vitamin Boost',
                'category': 'Supplement',
                'market': 'Japan',
                'channel': 'brand_website',
                'priceTier': 'premium',
                'visibleClaims': ['Preservative-free', 'Sealed nitrogen-filled stick'],
                'trustMarkers': ['Preservative-free seal', '30-day freshness guarantee'],
                'colorPalette': ['#F7F4ED', '#2C3E50', '#C9C2B3'],
                'packagingStyle': 'Single-dose sealed sticks in a clean carton',
                'hierarchyPattern': [
                    'Preservative-free seal', 'Active ingredient amount',
                    'Brand mark', 'Daily count', 'Compliance',
                ],
                'typographyStyle': 'Editorial serif headline + clean gothic body',
                'imageryStyle': 'Macro shot of single dose, no people',
                'sustainabilitySignals': ['Recyclable secondary carton'],
                'originSignals': ['Made in Japan'],
                'functionalSignals': ['Preservative-free', 'Daily dose'],
                'emotionalSignals': ['Quiet confidence'],
                'riskNotes': [],
                'sourceType': 'brand_website',
            },
            {
                'brandName': 'Asahi Dear-Natura',
                'productName': 'Dear-Natura Style Multivitamin',
                'category': 'Supplement',
                'market': 'Japan',
                'channel': 'amazon',
                'priceTier': 'mainstream',
                'visibleClaims': ['11 vitamins · 9 minerals', '60日分'],
                'trustMarkers': ['Reviewed for Japan market', 'JHFA-style seal'],
                'colorPalette': ['#FFFFFF', '#0F2E5C', '#E8A33D'],
                'packagingStyle': 'Square-shouldered HDPE bottle, large typographic front',
                'hierarchyPattern': [
                    'Vitamin/mineral count', 'Daily-dose count',
                    'Brand mark', 'Capsule shape illustration', 'Compliance line',
                ],
                'typographyStyle': 'Bold gothic numerals + small Japanese body',
                'imageryStyle': 'Capsule cross-section line illustration',
                'sustainabilitySignals': [],
                'originSignals': ['Made in Japan'],
                'functionalSignals': ['11 vitamins', '9 minerals', '60-day supply'],
                'emotionalSignals': [],
                'riskNotes': ['Avoids "boost"/"energy" — sticks to compositional facts.'],
                'sourceType': 'amazon',
            },
        ],
        'commonPatterns': {
            'claims': ['Quantified day-supply', 'Specific mg/IU amounts', '"Made in Japan"'],
            'colors': ['#FFFFFF dominant', 'navy / black secondary', 'gold accent for trust'],
            'trustMarkers': ['GMP / JAS / preservative-free seals', 'Daily-dose counts'],
            'hierarchy': [
                'Quantified active first', 'Day-supply second',
                'Brand mark third', 'Compliance line bottom',
            ],
            'packagingStyles': ['Compact pouches/sticks', 'Square-shouldered HDPE bottles'],
            'typography': ['Conservative gothic + Mincho for legal'],
            'imagery': ['Typographic-only or single capsule illustration; no lifestyle people'],
            'priceSignals': ['White-dominant = mainstream; warm beige + serif = premium'],
        },
        'whiteSpaceOpportunities': [
            'Western-sourced provenance with documented purity',
            'Single hero number + restrained typography (between Asahi mass and FANCL premium)',
            'Allergen and additive transparency above pharmacy norm',
        ],
        'overusedPatterns': [
            'Generic green leaf / nature imagery',
            'Hype words ("boost", "energy")',
            'Heavy multilingual front-of-pack',
        ],
        'adaptationImplications': [
            'Lead with mg / day-supply — buyers scan for numbers, not stories',
            'Drop English hype copy; use clean Japanese functional language',
            'Conservative palette (white + navy or warm beige); reserve color for the cap or one accent',
        ],
    },

    # ============== 2) Protein bar entering Korea ==============
    ('Food', 'South Korea'): {
        'referenceProducts': [
            {
                'brandName': 'Allmax / Bodylux (KR import)',
                'productName': '20g Whey Protein Bar',
                'category': 'Food',
                'market': 'South Korea',
                'channel': 'amazon',
                'priceTier': 'premium',
                'visibleClaims': ['20g 단백질', 'Low sugar', 'Lab-tested'],
                'trustMarkers': ['Lab-tested seal', 'Hangul nutrition table', 'D2C review count cue'],
                'colorPalette': ['#0A0A0A', '#FAF7F2', '#4ECDC4'],
                'packagingStyle': 'Foil wrap with strong typographic hero',
                'hierarchyPattern': [
                    'Quantified protein (g)', 'Sugar callout', 'Brand mark',
                    'Lab-tested seal', 'Compliance + importer',
                ],
                'typographyStyle': 'Tight geometric sans + condensed Hangul',
                'imageryStyle': 'Macro shot of bar cross-section',
                'sustainabilitySignals': [],
                'originSignals': ['Imported · USA'],
                'functionalSignals': ['20g protein', '<3g sugar', 'Lab-tested'],
                'emotionalSignals': ['Lifestyle wellness cue'],
                'riskNotes': [],
                'sourceType': 'amazon',
            },
            {
                'brandName': 'Olive Young Wellness',
                'productName': 'OY Protein Snack 12g',
                'category': 'Food',
                'market': 'South Korea',
                'channel': 'health_store',
                'priceTier': 'mainstream',
                'visibleClaims': ['12g protein', 'Daily snack', 'K-Wellness'],
                'trustMarkers': ['Olive Young exclusive', 'Hangul ingredient list', 'Allergen icons'],
                'colorPalette': ['#FFFFFF', '#FF6B9D', '#0A0A0A'],
                'packagingStyle': 'Soft-touch matte pouch with photographic flat-lay',
                'hierarchyPattern': [
                    'Lifestyle hero claim', 'Quantified protein',
                    'Brand mark', 'K-Wellness cue', 'Compliance',
                ],
                'typographyStyle': 'Playful rounded sans + script accent',
                'imageryStyle': 'Pastel flat-lay, occasional young female hand',
                'sustainabilitySignals': ['Mono-material pouch'],
                'originSignals': ['Made in Korea'],
                'functionalSignals': ['12g protein', 'Vegan'],
                'emotionalSignals': ['Lifestyle, Instagram-shareable'],
                'riskNotes': [],
                'sourceType': 'health_store',
            },
            {
                'brandName': 'Coupang Rocket Fresh',
                'productName': 'Rocket Protein Bar Variety',
                'category': 'Food',
                'market': 'South Korea',
                'channel': 'local_ecommerce',
                'priceTier': 'mainstream',
                'visibleClaims': ['15g protein', '10-pack value'],
                'trustMarkers': ['Coupang Rocket fast-delivery badge', '10-pack callout'],
                'colorPalette': ['#FFD400', '#0A0A0A', '#FFFFFF'],
                'packagingStyle': 'Multi-pack outer box, individual bars in foil',
                'hierarchyPattern': [
                    'Protein gram count', 'Pack count',
                    'Brand mark', 'Rocket delivery badge', 'Compliance',
                ],
                'typographyStyle': 'Bold gothic + thumbnail-readable numerals',
                'imageryStyle': 'Photo of full bar + cross-section + pack shot',
                'sustainabilitySignals': [],
                'originSignals': ['Made in Korea'],
                'functionalSignals': ['15g protein', '10-count'],
                'emotionalSignals': ['Value / convenience'],
                'riskNotes': [],
                'sourceType': 'local_ecommerce',
            },
        ],
        'commonPatterns': {
            'claims': ['Quantified protein (g)', 'Sugar callout', 'Pack-size value'],
            'colors': ['Black hero + white base + one warm accent (rose/teal/yellow)'],
            'trustMarkers': ['Lab-tested seal', 'Hangul ingredient list', 'D2C review count'],
            'hierarchy': [
                'Quantified protein first', 'Functional/lifestyle hero second',
                'Brand mark', 'Trust seal', 'Compliance + importer',
            ],
            'packagingStyles': ['Foil wrap', 'Soft-touch matte pouches', 'Variety multi-pack'],
            'typography': ['Tight geometric sans + condensed Hangul'],
            'imagery': ['Cross-section macro or pastel flat-lay'],
            'priceSignals': ['Black + accent = premium; bright yellow = value'],
        },
        'whiteSpaceOpportunities': [
            'Lifestyle wellness positioning with documented lab testing (between OY mass and US-import premium)',
            'Mono-material packaging + provenance story',
            'Functional benefit with K-Wellness lifestyle cue instead of clinical pharmacy aesthetic',
        ],
        'overusedPatterns': [
            'Pure clinical / pharmacy aesthetic for D2C wellness',
            'Generic Western wellness stock photography',
            'Underspecified "supports health" claims',
        ],
        'adaptationImplications': [
            'Quantify protein and sugar visibly in Hangul + numerals',
            'Replace clinical typography with tighter K-Wellness lifestyle treatment',
            'Add an importer field and Hangul ingredient list as table-stakes trust signals',
        ],
    },

    # ============== 3) Instant noodles entering Germany ==============
    ('Food', 'Germany'): {
        'referenceProducts': [
            {
                'brandName': 'Nissin (DE)',
                'productName': 'Cup Noodles Curry',
                'category': 'Food',
                'market': 'Germany',
                'channel': 'supermarket',
                'priceTier': 'mainstream',
                'visibleClaims': ['Fertig in 3 Minuten', 'Ohne Geschmacksverstärker'],
                'trustMarkers': ['German nutrition declaration', 'EU allergen panel', 'Recycle codes'],
                'colorPalette': ['#FFD400', '#C8102E', '#FFFFFF'],
                'packagingStyle': 'Cylindrical paper cup, photographic hero',
                'hierarchyPattern': [
                    'Flavor name', 'Photographic hero shot',
                    'Brand mark', '3-minute callout', 'EU allergen panel',
                ],
                'typographyStyle': 'Bold gothic + Latin-style flavor name',
                'imageryStyle': 'Steam-rising bowl photography',
                'sustainabilitySignals': ['Recyclable paper cup'],
                'originSignals': ['Made in Hungary for EU market'],
                'functionalSignals': ['3-minute preparation', 'No flavor enhancers'],
                'emotionalSignals': ['Convenience'],
                'riskNotes': ['"Ohne Geschmacksverstärker" requires substantiation under FIC.'],
                'sourceType': 'supermarket',
            },
            {
                'brandName': 'Yum Yum (DE Import)',
                'productName': 'Yum Yum Tom Yum Cup',
                'category': 'Food',
                'market': 'Germany',
                'channel': 'supermarket',
                'priceTier': 'budget',
                'visibleClaims': ['Authentisches Thai-Rezept', '3 Min.'],
                'trustMarkers': ['Country-of-origin: Thailand', 'EU allergen panel'],
                'colorPalette': ['#E81E25', '#FFD400', '#FFFFFF'],
                'packagingStyle': 'Bright cylindrical cup with stylised lettering',
                'hierarchyPattern': [
                    'Flavor name (Thai)', 'Hero photo', 'Brand mark',
                    'Prep time', 'Compliance',
                ],
                'typographyStyle': 'Display latin + stylised Thai accent',
                'imageryStyle': 'Photographic bowl + chili',
                'sustainabilitySignals': [],
                'originSignals': ['Made in Thailand'],
                'functionalSignals': ['Authentic origin', '3-minute prep'],
                'emotionalSignals': ['Travel/exotic'],
                'riskNotes': [],
                'sourceType': 'supermarket',
            },
            {
                'brandName': 'Edeka Bio Wellness',
                'productName': 'Edeka Bio Asia-Style Nudeln',
                'category': 'Food',
                'market': 'Germany',
                'channel': 'supermarket',
                'priceTier': 'premium',
                'visibleClaims': ['Bio', 'Vegan', 'Ohne Palmöl'],
                'trustMarkers': ['EU Bio logo', 'Vegan-mark', 'Edeka private-label'],
                'colorPalette': ['#F5F5F0', '#2E7D32', '#1A1A1A'],
                'packagingStyle': 'Restrained card + recyclable cup',
                'hierarchyPattern': [
                    'Bio + Vegan seals', 'Variant name', 'Brand mark',
                    'Ingredient transparency', 'EU compliance',
                ],
                'typographyStyle': 'Restrained sans + small serif for trust line',
                'imageryStyle': 'Ingredient-led illustration; no people',
                'sustainabilitySignals': ['EU Bio logo', 'Ohne Palmöl'],
                'originSignals': ['Hergestellt in Deutschland'],
                'functionalSignals': ['Bio certification', 'Vegan'],
                'emotionalSignals': ['Quiet quality'],
                'riskNotes': [],
                'sourceType': 'supermarket',
            },
        ],
        'commonPatterns': {
            'claims': ['Prep time minutes', 'Substantiated organic / vegan / palm-oil-free claims'],
            'colors': ['Bright red/yellow for mainstream Asian flavor; muted green/beige for premium Bio'],
            'trustMarkers': ['EU Bio logo', 'EU allergen panel', 'German nutrition declaration'],
            'hierarchy': [
                'Flavor/variant name', 'Photographic hero or certification',
                'Brand mark', 'Prep time', 'EU compliance + allergens',
            ],
            'packagingStyles': ['Cylindrical paper cup', 'Restrained recyclable card-and-cup'],
            'typography': ['Bold gothic for mainstream', 'restrained sans + serif accent for Bio'],
            'imagery': ['Steam-rising bowl photography or ingredient illustration'],
            'priceSignals': ['Saturated red/yellow = budget; muted green/beige + Bio = premium'],
        },
        'whiteSpaceOpportunities': [
            'Imported Korean noodle with EU-compliant restraint instead of bright Asian hype',
            'Documented sustainability (palm-oil-free, recyclable cup) over generic flavor copy',
            'Single hero functional callout in German over crowded multilingual',
        ],
        'overusedPatterns': [
            'Hyper-saturated red/yellow on shelf — visually fatigued in DE',
            'English hype words ("amazing", "best") on the front',
            'Generic "100% natural" without certification',
        ],
        'adaptationImplications': [
            'Lead in German with one substantiated claim (Bio / Vegan / ohne Palmöl)',
            'Cool the palette: drop hyper-saturated reds; lean restrained green/beige if Bio is true',
            'Move flavor name above brand mark for shelf scan; keep allergen panel non-negotiable',
        ],
    },

    # ============== 4) Premium Nordic food entering UAE ==============
    ('Food', 'UAE'): {
        'referenceProducts': [
            {
                'brandName': 'Carrefour Selection',
                'productName': 'Smoked Norwegian Salmon',
                'category': 'Food',
                'market': 'UAE',
                'channel': 'supermarket',
                'priceTier': 'premium',
                'visibleClaims': ['Wild-caught', 'Origin: Norway', 'No artificial preservatives'],
                'trustMarkers': ['Halal certification', 'Carrefour Selection mark', 'Norway flag origin'],
                'colorPalette': ['#0A2E5C', '#FFFFFF', '#C9A961'],
                'packagingStyle': 'Vacuum-sealed pack with rigid card sleeve',
                'hierarchyPattern': [
                    'Origin badge (Norway flag)', 'Product type',
                    'Halal cert', 'Brand mark', 'Arabic + English nutrition',
                ],
                'typographyStyle': 'Serif headline + tight gothic body (Arabic + English)',
                'imageryStyle': 'Macro shot of salmon slice on white',
                'sustainabilitySignals': ['Sustainably farmed'],
                'originSignals': ['Origin: Norway', 'Wild-caught'],
                'functionalSignals': ['No preservatives'],
                'emotionalSignals': ['Provenance, restraint'],
                'riskNotes': ['Halal cert is non-negotiable in UAE supermarket channel.'],
                'sourceType': 'supermarket',
            },
            {
                'brandName': 'Spinneys Finest',
                'productName': 'Spinneys Nordic-style Crackers',
                'category': 'Food',
                'market': 'UAE',
                'channel': 'supermarket',
                'priceTier': 'premium',
                'visibleClaims': ['Made in Sweden', 'Whole-grain'],
                'trustMarkers': ['Spinneys Finest mark', 'Halal cert', 'Bilingual ingredient list'],
                'colorPalette': ['#1F2937', '#F5F2EC', '#C9A961'],
                'packagingStyle': 'Restrained matte carton with embossed brand mark',
                'hierarchyPattern': [
                    'Provenance badge', 'Variant name (Arabic + English)',
                    'Brand mark', 'Halal cert', 'Bilingual compliance',
                ],
                'typographyStyle': 'Editorial serif + matched Arabic naskh',
                'imageryStyle': 'Single-cracker macro on slate',
                'sustainabilitySignals': ['Recyclable carton'],
                'originSignals': ['Made in Sweden'],
                'functionalSignals': ['Whole-grain'],
                'emotionalSignals': ['Quiet luxury, gift-ready'],
                'riskNotes': [],
                'sourceType': 'supermarket',
            },
            {
                'brandName': 'Noon (Marketplace)',
                'productName': 'Nordic Premium Reindeer Jerky',
                'category': 'Food',
                'market': 'UAE',
                'channel': 'local_ecommerce',
                'priceTier': 'luxury',
                'visibleClaims': ['Imported · Finland', 'Halal-certified', 'Single-source'],
                'trustMarkers': ['Halal cert', 'Country-of-origin lockup', 'Importer field'],
                'colorPalette': ['#0A0A0A', '#C9A961', '#FAF7F2'],
                'packagingStyle': 'Matte black pouch with foil accents',
                'hierarchyPattern': [
                    'Origin (Finland)', 'Single-source line',
                    'Halal cert', 'Brand mark', 'Importer + compliance',
                ],
                'typographyStyle': 'Editorial serif + Arabic naskh',
                'imageryStyle': 'Studio shot of single jerky strip on dark slate',
                'sustainabilitySignals': ['Single-source provenance'],
                'originSignals': ['Imported · Finland'],
                'functionalSignals': ['Single-source quality'],
                'emotionalSignals': ['Luxury, tourist-gift'],
                'riskNotes': ['Reindeer is a sensitive ingredient — confirm import permit.'],
                'sourceType': 'local_ecommerce',
            },
        ],
        'commonPatterns': {
            'claims': ['Origin / provenance line', 'Halal cert', 'Bilingual variant name'],
            'colors': ['Navy + white + gold (premium); black + gold (luxury)'],
            'trustMarkers': ['Halal certification', 'Origin badge', 'Bilingual ingredient list'],
            'hierarchy': [
                'Origin badge', 'Variant name (AR + EN)',
                'Halal cert', 'Brand mark', 'Bilingual compliance',
            ],
            'packagingStyles': ['Vacuum-sealed pack + sleeve', 'Matte black foil pouch'],
            'typography': ['Editorial serif + Arabic naskh of matched weight'],
            'imagery': ['Single-product macro on dark or neutral background'],
            'priceSignals': ['Navy + gold = premium; matte black + gold = luxury'],
        },
        'whiteSpaceOpportunities': [
            'Documented Nordic provenance + Halal cert — combine restraint with explicit trust',
            'Gift-ready secondary carton for tourist channel',
            'Origin story in Arabic, not transliterated English',
        ],
        'overusedPatterns': [
            'Western-only English packs without Arabic typography',
            'Bright lifestyle photography in a category that rewards restraint',
            'Halal cert relegated to back of pack',
        ],
        'adaptationImplications': [
            'Halal certification must appear front-of-pack',
            'Bilingual (AR + EN) flavor / variant name in matched typography weights',
            'Quiet palette (navy + gold or black + gold); reserve color for one accent',
        ],
    },

    # ============== 5) Functional drink entering USA ==============
    ('Beverage', 'USA'): {
        'referenceProducts': [
            {
                'brandName': 'Liquid Death',
                'productName': 'Liquid Death Mountain Water',
                'category': 'Beverage',
                'market': 'USA',
                'channel': 'amazon',
                'priceTier': 'premium',
                'visibleClaims': ['Mountain water', 'Infinitely recyclable can'],
                'trustMarkers': ['BPA-free can', 'Carbon-neutral certification'],
                'colorPalette': ['#050505', '#FFFFFF', '#DC2626'],
                'packagingStyle': 'Aluminum can with edgy display lettering',
                'hierarchyPattern': [
                    'Brand mark (giant)', 'Product type',
                    'Recyclable / sustainability cue', 'Volume', 'Compliance',
                ],
                'typographyStyle': 'Heavy display blackletter + tight gothic',
                'imageryStyle': 'Typographic only — no lifestyle imagery',
                'sustainabilitySignals': ['Infinitely recyclable can', 'Carbon-neutral'],
                'originSignals': [],
                'functionalSignals': ['Hydration'],
                'emotionalSignals': ['Brand cult / distinctive identity'],
                'riskNotes': [],
                'sourceType': 'amazon',
            },
            {
                'brandName': 'Olipop',
                'productName': 'Olipop Strawberry Vanilla',
                'category': 'Beverage',
                'market': 'USA',
                'channel': 'supermarket',
                'priceTier': 'premium',
                'visibleClaims': ['9g fiber', '<5g sugar', 'Supports gut health*'],
                'trustMarkers': ['Third-party tested', 'Non-GMO', 'FDA disclaimer footnote'],
                'colorPalette': ['#F4C4D7', '#0F2E5C', '#FFFFFF'],
                'packagingStyle': '12oz can with retro-modern flat illustration',
                'hierarchyPattern': [
                    'Quantified functional benefit', 'Flavor variant',
                    'Brand mark', 'Trust seals', 'FDA disclaimer line',
                ],
                'typographyStyle': 'Retro display + clean modern body',
                'imageryStyle': 'Flat retro illustration of fruit/spice',
                'sustainabilitySignals': ['Recyclable can', 'Non-GMO'],
                'originSignals': [],
                'functionalSignals': ['9g fiber', '<5g sugar', 'Prebiotic'],
                'emotionalSignals': ['Lifestyle wellness'],
                'riskNotes': ['Asterisk + FDA disclaimer for functional claim.'],
                'sourceType': 'supermarket',
            },
            {
                'brandName': 'Celsius',
                'productName': 'Celsius Sparkling Orange',
                'category': 'Beverage',
                'market': 'USA',
                'channel': 'convenience',
                'priceTier': 'mainstream',
                'visibleClaims': ['Live Fit', '200mg caffeine', 'Zero sugar', 'Clinically proven*'],
                'trustMarkers': ['Informed-Sport seal', 'Non-GMO seal'],
                'colorPalette': ['#FF6B00', '#FFFFFF', '#0A0A0A'],
                'packagingStyle': 'Slim aluminum can with bold typography',
                'hierarchyPattern': [
                    'Brand mark (giant)', 'Functional callout', 'Flavor',
                    'Trust seals', 'FDA disclaimer line',
                ],
                'typographyStyle': 'Bold condensed gothic + accent stripe',
                'imageryStyle': 'Typographic + abstract burst graphic',
                'sustainabilitySignals': [],
                'originSignals': [],
                'functionalSignals': ['200mg caffeine', 'Zero sugar', 'Performance'],
                'emotionalSignals': ['Energy / performance'],
                'riskNotes': ['"Clinically proven" requires citable trial; FDA asterisk in use.'],
                'sourceType': 'convenience_store',
            },
        ],
        'commonPatterns': {
            'claims': ['Quantified functional benefit', 'Zero sugar', 'Caffeine mg'],
            'colors': ['High-contrast black + accent', 'pastel illustration for premium gut-health'],
            'trustMarkers': ['Third-party tested', 'Non-GMO', 'FDA-disclaimer asterisk'],
            'hierarchy': [
                'Brand mark or quantified hero', 'Functional callout',
                'Flavor', 'Trust seal', 'FDA disclaimer',
            ],
            'packagingStyles': ['12oz can with retro illustration', 'slim can with display type'],
            'typography': ['Heavy display + clean body'],
            'imagery': ['Flat retro illustration or typographic only'],
            'priceSignals': ['Pastel illustration = premium; bold display + neon = mainstream/energy'],
        },
        'whiteSpaceOpportunities': [
            'Sustainably-sourced functional beverage with documented provenance — most US D2C skips origin',
            'Single quantified active + clean illustration between hype-display and pastel-illustration extremes',
            'Lower-caffeine adaptogenic positioning for older buyers',
        ],
        'overusedPatterns': [
            'Pastel "wellness" gradient illustration on every gut-health brand',
            'Black-display "edgy" without a real reason-to-believe',
            'Unsubstantiated "clinically proven" without an FDA asterisk',
        ],
        'adaptationImplications': [
            'Quantify the functional active in mg / g — US buyers scan for numbers',
            'Add an FDA-style disclaimer line if any functional claim is shown',
            'Pick ONE visual lane (typographic / illustrative) — do not mix retro illustration with display blackletter',
        ],
    },
}


def _fallback_summary(category: str, target_market: str, channel: str) -> MarketReferenceSummary:
    """
    For combos without hand-written reference data, return a thin but plausible
    fallback so the agents and prompt always have something to consume.
    """
    return {
        'targetMarket': target_market,
        'category': category,
        'channel': channel,
        'referenceProducts': [],
        'commonPatterns': {
            'claims': ['Quantified functional benefit', 'Clear allergen / ingredient transparency'],
            'colors': ['Restrained neutral base + one accent encoding the benefit'],
            'trustMarkers': ['Local-language ingredient list', 'Origin / provenance line'],
            'hierarchy': [
                'Quantified hero benefit', 'Product type / variant',
                'Brand mark', 'Trust signal', 'Compliance line',
            ],
            'packagingStyles': ['Category-native primary package'],
            'typography': ['Confident sans + restrained accent face'],
            'imagery': ['Single-product macro on neutral background'],
            'priceSignals': ['Restraint reads premium; saturation reads mainstream'],
        },
        'whiteSpaceOpportunities': [
            f"Quantified, restrained niche for {category.lower()} in {target_market}",
            'Documented provenance vs. unstoried import competitors',
        ],
        'overusedPatterns': [
            'Generic Western lifestyle photography',
            'Unsubstantiated "natural" or "premium" claims',
        ],
        'adaptationImplications': [
            'Lead with one quantified benefit and one trust signal',
            'Match the channel\'s visual density norm — pharmacy ≠ supermarket ≠ Amazon thumbnail',
        ],
        'source': 'mock-fallback',
    }


def get_competitor_references(
    product_name: str,
    product_category: str,
    target_market: str,
    target_channel: str,
    target_buyer: str = '',
    price_tier: str = '',
    brand_goal: str = '',
) -> MarketReferenceSummary:
    """
    Return mock competitor reference data for the (category, market) combo.

    The signature accepts every field the brief promises but only (category,
    market, channel) currently affect the result — extra fields are reserved
    for the live-data future (e.g. price_tier filters the reference set).

    TODO (live):
        - Replace the dict lookup with a fan-out to retail/marketplace
          adapters (Amazon PA-API, Rakuten, Coupang, Olive Young, etc.)
        - Filter the returned references by price_tier and brand_goal.
        - Add `freshness_days` per reference for staleness scoring.
    """
    key = (product_category, target_market)
    if key in _MOCK_REFERENCES:
        data = dict(_MOCK_REFERENCES[key])
        summary: MarketReferenceSummary = {
            'targetMarket': target_market,
            'category': product_category,
            'channel': target_channel or _priority_channels_for_category(product_category, '')[0],
            'referenceProducts': data.get('referenceProducts', []),
            'commonPatterns': data.get('commonPatterns', {}),
            'whiteSpaceOpportunities': data.get('whiteSpaceOpportunities', []),
            'overusedPatterns': data.get('overusedPatterns', []),
            'adaptationImplications': data.get('adaptationImplications', []),
            'source': 'mock',
        }
        return summary

    return _fallback_summary(
        product_category,
        target_market,
        target_channel or _priority_channels_for_category(product_category, '')[0],
    )


# ----------------------------------------------------------------------------
# Helper for the orchestrator + agent layer: derive a compact
# `marketReferenceInsights` dict that fits straight into adaptationBrief.
# ----------------------------------------------------------------------------

def to_market_reference_insights(summary: MarketReferenceSummary) -> dict:
    cp = summary.get('commonPatterns') or {}
    return {
        'categoryNorms': cp.get('claims', [])[:4] + cp.get('hierarchy', [])[:2],
        'trustMarkersToConsider': cp.get('trustMarkers', [])[:5],
        'visualPatternsToRespect': cp.get('packagingStyles', [])[:3] + cp.get('imagery', [])[:2],
        'patternsToAvoid': summary.get('overusedPatterns', [])[:5],
        'differentiationOpportunities': summary.get('whiteSpaceOpportunities', [])[:4],
        'retailChannelExpectations': cp.get('priceSignals', [])[:3] + cp.get('hierarchy', [])[2:5],
    }
