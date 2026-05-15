"""Competitor & Shelf Positioning Agent — likely competitive set and angle."""

from .base import BaseAgent, market_context
from .types import AnalysisInput, AgentOutput


# Sketches per (target_market, category). Kept descriptive (textual) per the brief.
COMPETITIVE_SETS = {
    ('Japan', 'Supplement'): {
        'set': [
            'DHC (mass pharmacy / convenience)',
            'Asahi Dear-Natura (mainstream supplement)',
            'FANCL (premium D2C wellness)',
        ],
        'angle': 'Foreign-imported provenance with documented purity is the differentiation angle vs domestic pharmacy brands.',
    },
    ('Germany', 'Food'): {
        'set': [
            'Demeter / Alnatura (premium organic mainstream)',
            'Edeka private label (mainstream supermarket)',
            'dm Bio (mass-market organic pharmacy-like)',
        ],
        'angle': 'Lean on origin, sustainability certifications, and restraint over flavor hype.',
    },
    ('South Korea', 'Supplement'): {
        'set': [
            'Anua / Numbuzin (K-Beauty-adjacent wellness)',
            'CJW (mainstream supplement)',
            'Olive Young private wellness lines',
        ],
        'angle': 'Quantified beauty/wellness positioning with K-Wellness lifestyle cues, not pharmacy.',
    },
}


class CompetitorPositioningAgent(BaseAgent):
    id = 'competitiveFit'
    label = 'Competitor & Shelf Positioning Agent'

    def run(self, input: AnalysisInput) -> AgentOutput:
        ctx = market_context(input.get('target_market', ''))
        cat = input.get('product_category', 'Food')
        tm = input.get('target_market', '')
        score = self.stable_score(input, lo=55, hi=82)

        # Prefer observed competitor refs when present — they're market-real.
        refs = input.get('marketReferences') or {}
        ref_products = refs.get('referenceProducts') or []
        if ref_products:
            competitive_set = [
                f"{r.get('brandName', '?')} — {r.get('productName', '')} ({r.get('priceTier', '?')})"
                for r in ref_products[:3]
            ]
            implications = refs.get('adaptationImplications') or []
            whitespace = refs.get('whiteSpaceOpportunities') or []
            angle = whitespace[0] if whitespace else (
                implications[0] if implications else
                f"Own a quantified, restrained niche between premium-local and mass-import in {tm}."
            )
        else:
            ref = COMPETITIVE_SETS.get((tm, cat))
            if ref:
                competitive_set = ref['set']
                angle = ref['angle']
            else:
                competitive_set = [
                    f"Local premium {cat.lower()} brands focused on origin storytelling",
                    f"Mainstream {cat.lower()} brands focused on price-value clarity",
                    f"D2C / channel-native {cat.lower()} brands with quantified claims",
                ]
                angle = f"Own a quantified, restrained niche between premium-local and mass-import in {tm}."

        findings = [
            f"Likely competitive set in {tm}: {competitive_set[0]}",
            'Current label reads as a foreign export rather than a locally positioned product.',
            'Premium claim is unsupported by visual or compositional evidence on pack.',
        ]
        recommendations = [
            f"Differentiate via: {angle}",
            'Add one verifiable, specific provenance line.',
            'Reduce visual elements to read as confidently as premium-local competitors.',
        ]

        return {
            'agent': self.id,
            'score': score,
            'findings': findings,
            'recommendations': recommendations,
            'detail': {
                'likelyCompetitiveSet': competitive_set,
                'currentPositioning': 'Generic premium-import',
                'recommendedPositioning': f"Premium imported {cat.lower()} with documented provenance and restrained design",
                'differentiationAngle': angle,
                'competitorReferences': competitive_set[:3],
            },
        }
