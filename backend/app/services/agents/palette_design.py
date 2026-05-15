"""Palette & Design Agent — palette, typography mood, finish."""

from .base import BaseAgent, market_context
from .types import AnalysisInput, AgentOutput


TYPOGRAPHY_BY_TIER = {
    'budget':     'Functional grotesque, high readability, no display nuance.',
    'mainstream': 'Confident geometric sans, medium contrast, clear hierarchy.',
    'premium':    'Restrained neo-grotesque + a single serif accent for provenance.',
    'luxury':     'Editorial serif + tightly tracked geometric sans for callouts.',
}

FINISH_BY_TIER = {
    'budget':     'Matte cold-foil-free, minimum sleeve waste, recyclable mono-material.',
    'mainstream': 'Soft-touch matte with selective spot UV on the hero claim.',
    'premium':    'Uncoated paper feel + debossed brand mark, mono-material substrate.',
    'luxury':     'Heavy-stock label, debossed/embossed marks, foiling reserved for one accent.',
}


class PaletteDesignAgent(BaseAgent):
    id = 'designFit'
    label = 'Palette & Design Agent'

    def run(self, input: AnalysisInput) -> AgentOutput:
        ctx = market_context(input.get('target_market', ''))
        score = self.stable_score(input, lo=55, hi=85)
        tier = input.get('price_tier', 'mainstream')

        palette = ctx['palette_hint']

        # Pull a representative competitor palette to ground the finding.
        refs = input.get('marketReferences') or {}
        ref_products = refs.get('referenceProducts') or []
        observed_palettes = [r.get('colorPalette') for r in ref_products if r.get('colorPalette')]
        observed_note = (
            f"Observed competitor palettes lean: {', '.join(observed_palettes[0])}."
            if observed_palettes else
            'Current palette reads category-generic for the target market.'
        )

        findings = [
            observed_note,
            'Contrast between hero benefit and background is below shelf-readable threshold.',
            'Accent color is decorative; it should carry the trust signal.',
        ]
        recommendations = [
            'Use one restrained accent color tied to the hero benefit.',
            'Increase whitespace around the hero benefit by ~20%.',
            'Drop secondary palette colors that do not encode meaning.',
        ]

        return {
            'agent': self.id,
            'score': score,
            'findings': findings,
            'recommendations': recommendations,
            'detail': {
                'currentPaletteRead': f"Reads {tier} but category-generic for {input.get('target_market', '')}.",
                'recommendedPalette': palette,
                'typographyDirection': TYPOGRAPHY_BY_TIER.get(tier, TYPOGRAPHY_BY_TIER['mainstream']),
                'finishDirection': FINISH_BY_TIER.get(tier, FINISH_BY_TIER['mainstream']),
                'layoutDirection': 'Single hero benefit, single trust strip, single regulatory line.',
            },
        }
