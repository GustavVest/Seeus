"""
Final Strategy Agent — synthesizes the 8 specialist outputs into the final
report JSON matching the product brief schema.

This agent does no LLM call (in scaffold mode); it derives the synthesis from
the agent outputs deterministically.
"""

from typing import Dict, List, Optional

from .types import AnalysisInput, AgentOutput, FinalReport, AGENT_WEIGHTS
from .base import market_context
from .competitor_references import (
    MarketReferenceSummary,
    to_market_reference_insights,
)
from .style_modes import style_mode_spec, brand_type_spec


def _weighted_overall(scores: Dict[str, int]) -> int:
    total = sum(scores.get(k, 0) * w for k, w in AGENT_WEIGHTS.items())
    return int(round(total))


def _summary(input: AnalysisInput, overall: int, biggest_weak: str) -> str:
    band = (
        'Strong overall fit' if overall >= 80
        else 'Workable but needs targeted fixes' if overall >= 65
        else 'High friction — significant rework needed'
    )
    return (
        f"{band} for {input.get('product_name', 'this product')} entering "
        f"{input.get('target_market', 'the target market')}. "
        f"Biggest current weakness: {biggest_weak.lower()}."
    )


def synthesize(
    input: AnalysisInput,
    agent_outputs: Dict[str, AgentOutput],
    market_references: Optional[MarketReferenceSummary] = None,
) -> FinalReport:
    """Combine all 8 agent outputs into the final report JSON."""

    agent_scores = {
        'cultureFit':       agent_outputs['cultureFit']['score'],
        'trendFit':         agent_outputs['trendFit']['score'],
        'claimsSafety':     agent_outputs['claimsSafety']['score'],
        'visualHierarchy':  agent_outputs['visualHierarchy']['score'],
        'designFit':        agent_outputs['designFit']['score'],
        'competitiveFit':   agent_outputs['competitiveFit']['score'],
        'buyerMotivation':  agent_outputs['buyerMotivation']['score'],
        'exportReadiness':  agent_outputs['exportReadiness']['score'],
    }
    overall = _weighted_overall(agent_scores)

    # Strongest / weakest by raw score
    sorted_by_score = sorted(agent_scores.items(), key=lambda kv: kv[1])
    weakest = sorted_by_score[0][0]
    strongest = sorted_by_score[-1][0]

    # Priority fixes: pull the first recommendation from each of the 3 weakest agents.
    priority_fixes: List[str] = []
    for agent_id, _ in sorted_by_score[:3]:
        recs = agent_outputs[agent_id].get('recommendations', [])
        if recs:
            priority_fixes.append(recs[0])

    # Risk flags from claims agent
    risk_flags = agent_outputs['claimsSafety'].get('detail', {}).get('flags', [])

    # Recommended positioning + headline + sub from the buyer agent
    buyer_detail = agent_outputs['buyerMotivation'].get('detail', {})
    headline = buyer_detail.get('recommendedHeadline', '')
    sub = buyer_detail.get('recommendedSubheadline', '')
    positioning = agent_outputs['competitiveFit'].get('detail', {}).get(
        'recommendedPositioning', ''
    )

    # Palette + hierarchy + claims from their respective agents
    palette = agent_outputs['designFit'].get('detail', {}).get('recommendedPalette', {})
    hierarchy = agent_outputs['visualHierarchy'].get('detail', {}).get(
        'recommendedFrontHierarchy', []
    )

    # Build claims direction from claims_safety
    safer_claims = [
        f.get('suggested_alternative') for f in risk_flags
        if f.get('suggested_alternative')
    ]
    claims_to_avoid = [
        f.get('phrase') for f in risk_flags
        if f.get('level') in ('red', 'yellow') and f.get('phrase')
    ]

    # Trust markers from market context
    ctx = market_context(input.get('target_market', ''))
    trust_markers = ctx.get('trust_markers', [])

    summary = _summary(input, overall, weakest)

    recommended_palette = {
        'primary':    palette.get('primary', ''),
        'secondary':  palette.get('secondary', ''),
        'accent':     palette.get('accent', ''),
        'background': palette.get('background', ''),
        'warning':    palette.get('warning', ''),
    }

    # Visual style mode + brand type overlays — pulled once, applied to
    # palette / design direction / style constraints.
    style_mode = (input.get('visual_style_mode') or 'Keep current brand style').strip()
    brand_type = (input.get('brand_type') or 'Own brand').strip()
    style_spec = style_mode_spec(style_mode)
    brand_spec = brand_type_spec(brand_type)

    # Apply palette overlay (gradient / metallicAccent) for expressive modes.
    for k, v in (style_spec.get('paletteOverlay') or {}).items():
        recommended_palette[k] = v

    # Compose the final design direction (style mode wins, agent layoutDirection
    # is the fallback when style mode is "Keep current brand style").
    agent_design_direction = (
        agent_outputs['designFit'].get('detail', {}).get('layoutDirection', '') or
        'Single hero benefit, single trust strip, single regulatory line.'
    )
    design_direction = (
        f"{style_spec.get('designDirection', '')} {agent_design_direction}"
    ).strip()

    must_preserve = [
        f"Product name: {input.get('product_name', '')}",
        f"Category: {input.get('product_category', '')}",
    ]
    ingredients = input.get('ingredients') or []
    if ingredients:
        must_preserve.append(f"Ingredient list: {', '.join(ingredients[:6])}")
    if input.get('country_of_origin'):
        must_preserve.append(f"Country of origin: {input['country_of_origin']}")
    # Verbatim claims the user typed in (e.g. "20g protein", "Low sugar",
    # "Gluten free"). These must NEVER be invented or altered downstream —
    # the image-gen mockup must keep these numbers bit-perfect.
    pack_claims = [c for c in (input.get('claims_on_pack') or []) if c]
    if pack_claims:
        must_preserve.append(
            'Quantified claims to keep bit-perfect: ' + '; '.join(pack_claims)
        )

    style_constraints = [
        f"Price tier reads: {input.get('price_tier', 'mainstream')}",
        f"Brand goal: {input.get('brand_goal', 'trust')}",
        f"Channel: {input.get('target_channel', 'supermarket')} — match its conventions",
    ]
    # Merge in the style-mode and brand-type constraints so the brief is
    # one self-contained source of truth.
    style_constraints += (style_spec.get('styleConstraints') or [])
    style_constraints += (brand_spec.get('styleConstraints') or [])
    forbidden_changes = [
        'Do not invent certifications, seals, or third-party logos',
        'Do not invent medical, disease-treatment, or disease-prevention claims',
        'Do not add ingredients that are not in the source label',
        'Do not produce illegible or nonsense typography',
        'Output is a concept mockup, not final compliant artwork',
    ]
    forbidden_changes += (style_spec.get('forbiddenStyles') or [])

    # Brand-asset preservation list. Defaults to a generic set since the agents
    # in scaffold mode don't read the image. A real Claude-vision extraction step
    # can populate this with specific assets pulled off the source label.
    brand_assets_to_preserve = [
        'logo',
        'brand name',
        'distinctive symbols and icon marks',
        'signature illustrations',
        'certification marks already present',
        'origin marks already present',
        'unique brand patterns or shapes',
    ]

    market_reference_insights = (
        to_market_reference_insights(market_references) if market_references else {}
    )

    # Surface the recommended label copy in the brief so the image prompt
    # can render the same headline/subhead/bullets the analysis recommended.
    recommended_label_copy_for_brief = {
        'frontLabelHeadline': headline or '',
        'subheadline': sub or '',
        'benefitBullets': agent_outputs['buyerMotivation']
            .get('detail', {})
            .get('missingElements', [])[:3],
        'trustMarkers': trust_markers[:4],
    }

    adaptation_brief = {
        'productName': input.get('product_name', ''),
        'category': input.get('product_category', ''),
        'brandType': brand_type,
        'visualStyleMode': style_mode,
        'targetMarket': input.get('target_market', ''),
        'targetChannel': input.get('target_channel', ''),
        'packageType': '',  # left to caller; could be set by image-extraction step
        'mustPreserve': must_preserve,
        'brandAssetsToPreserve': brand_assets_to_preserve,
        'claimsToAvoid': claims_to_avoid[:5],
        'saferClaims': safer_claims[:5],
        'palette': recommended_palette,
        'designDirection': design_direction,
        'hierarchy': hierarchy,
        'styleConstraints': style_constraints,
        'forbiddenChanges': forbidden_changes,
        'marketReferenceInsights': market_reference_insights,
        'recommendedLabelCopy': recommended_label_copy_for_brief,
    }

    report: FinalReport = {
        'product': {
            'name': input.get('product_name', ''),
            'category': input.get('product_category', ''),
            'targetMarket': input.get('target_market', ''),
            'targetChannel': input.get('target_channel', ''),
            'priceTier': input.get('price_tier', ''),
        },
        'overallMarketFitScore': overall,
        'summary': summary,
        'agentScores': agent_scores,
        'priorityFixes': priority_fixes,
        'riskFlags': risk_flags,
        'recommendedPositioning': positioning,
        'recommendedLabelCopy': {
            'frontLabelHeadline': headline,
            'subheadline': sub,
            'benefitBullets': agent_outputs['buyerMotivation']
                .get('detail', {})
                .get('missingElements', [])[:3],
            'trustMarkers': trust_markers[:4],
            'claimsToAvoid': claims_to_avoid[:5],
            'saferClaims': safer_claims[:5],
        },
        'recommendedPalette': recommended_palette,
        'recommendedHierarchy': hierarchy,
        'adaptationBrief': adaptation_brief,
        'marketReferences': market_references or {},
        'paidUpgradeSuggestion': 'Generate a market-adapted packaging mockup for this product and target market.',
        'agentOutputs': agent_outputs,
    }
    return report
