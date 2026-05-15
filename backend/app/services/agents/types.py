"""
Shared types for the market-fit agent system.

Plain Python dicts and typed literals. Each agent consumes an AnalysisInput
and produces an AgentOutput. The orchestrator combines outputs into a
FinalReport matching the JSON schema documented in the product brief.
"""

from typing import Optional, TypedDict, List, Literal


# ---------- Inputs ----------

# Note: 'Private Label' was removed from category in 2026-05.
# Private label is a brand type / business model, not a product category.
ProductCategory = Literal[
    'Supplement',
    'Beverage',
    'Food',
    'Snack',
    'Sauce / condiment',
    'Functional food',
    'Cosmetic / personal care',
    'Other',
]

BrandType = Literal[
    'Own brand',
    'Private label',
    'White label',
    'Distributor / importer brand',
    'Retailer brand',
]

VisualStyleMode = Literal[
    'Clean Premium',
    'Stylish Premium',
    'Bold Retail',
    'Clinical / Scientific',
    'Natural / Organic',
    'Luxury Minimal',
    'Trend-led / D2C',
    'Keep current brand style',
]

TargetChannel = Literal[
    'supermarket', 'pharmacy', 'convenience', 'amazon', 'specialty', 'b2b'
]
TargetBuyer = Literal[
    'mass', 'premium', 'health-conscious', 'athletes',
    'parents', 'elderly', 'gen-z', 'tourists', 'business',
]
PriceTier = Literal['budget', 'mainstream', 'premium', 'luxury']
BrandGoal = Literal[
    'trust', 'premium', 'functional', 'natural',
    'fun', 'clinical', 'local', 'export',
]


class AnalysisInput(TypedDict, total=False):
    # Image inputs (base64 PNG bytes, or None for scaffold runs)
    front_label_b64: Optional[str]
    back_label_b64: Optional[str]
    # Product descriptors
    product_name: str
    product_category: ProductCategory
    brand_type: BrandType
    visual_style_mode: VisualStyleMode
    ingredients: List[str]
    claims_on_pack: List[str]
    country_of_origin: str
    current_market: str
    target_market: str
    target_channel: TargetChannel
    target_buyer: TargetBuyer
    price_tier: PriceTier
    brand_goal: BrandGoal


# ---------- Agent output ----------

RiskLevel = Literal['green', 'yellow', 'red']


class RiskFlag(TypedDict, total=False):
    level: RiskLevel
    phrase: str
    issue: str
    suggested_alternative: Optional[str]


class AgentOutput(TypedDict, total=False):
    agent: str                 # canonical id, e.g. 'cultureFit'
    score: int                 # 0..100
    findings: List[str]        # what the agent saw
    recommendations: List[str] # concrete moves
    detail: dict               # agent-specific structured payload


# ---------- Final report shape ----------
# Matches the JSON schema in the product brief verbatim.

class ProductSummary(TypedDict):
    name: str
    category: str
    targetMarket: str
    targetChannel: str
    priceTier: str


class AgentScores(TypedDict):
    cultureFit: int
    trendFit: int
    claimsSafety: int
    visualHierarchy: int
    designFit: int
    competitiveFit: int
    buyerMotivation: int
    exportReadiness: int


class RecommendedPalette(TypedDict, total=False):
    primary: str
    secondary: str
    accent: str
    background: str
    warning: str
    # Optional, populated only for expressive style modes
    # (e.g. Stylish Premium uses gradient + metallicAccent).
    gradient: str
    metallicAccent: str


class RecommendedLabelCopy(TypedDict):
    frontLabelHeadline: str
    subheadline: str
    benefitBullets: List[str]
    trustMarkers: List[str]
    claimsToAvoid: List[str]
    saferClaims: List[str]


class MarketReferenceInsights(TypedDict, total=False):
    categoryNorms: List[str]
    trustMarkersToConsider: List[str]
    visualPatternsToRespect: List[str]
    patternsToAvoid: List[str]
    differentiationOpportunities: List[str]
    retailChannelExpectations: List[str]


class AdaptationBrief(TypedDict, total=False):
    productName: str
    category: str
    brandType: str
    visualStyleMode: str
    targetMarket: str
    targetChannel: str
    packageType: str
    mustPreserve: List[str]
    brandAssetsToPreserve: List[str]
    claimsToAvoid: List[str]
    saferClaims: List[str]
    palette: RecommendedPalette
    designDirection: str
    hierarchy: List[str]
    styleConstraints: List[str]
    forbiddenChanges: List[str]
    marketReferenceInsights: MarketReferenceInsights


class FinalReport(TypedDict, total=False):
    product: ProductSummary
    overallMarketFitScore: int
    summary: str
    agentScores: AgentScores
    priorityFixes: List[str]
    riskFlags: List[RiskFlag]
    recommendedPositioning: str
    recommendedLabelCopy: RecommendedLabelCopy
    recommendedPalette: RecommendedPalette
    recommendedHierarchy: List[str]
    adaptationBrief: AdaptationBrief
    marketReferences: dict   # MarketReferenceSummary from competitor_references
    paidUpgradeSuggestion: str
    # Per-agent raw outputs (useful for debug / paid upgrade detail views)
    agentOutputs: dict


# ---------- Weights used by orchestrator ----------

AGENT_WEIGHTS = {
    'cultureFit': 0.15,
    'trendFit': 0.10,
    'claimsSafety': 0.15,
    'visualHierarchy': 0.15,
    'designFit': 0.10,
    'competitiveFit': 0.10,
    'buyerMotivation': 0.10,
    'exportReadiness': 0.15,
}
