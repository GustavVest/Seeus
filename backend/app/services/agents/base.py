"""
Base agent interface + shared market/category context that scaffold outputs
can lean on to feel grounded.
"""

from __future__ import annotations
from typing import Optional
import hashlib

from .types import AnalysisInput, AgentOutput


class BaseAgent:
    """
    Subclasses implement run(input) -> AgentOutput.
    The base provides a stable, deterministic score helper so the same input
    produces the same scaffold output across runs.
    """

    id: str = 'baseAgent'
    label: str = 'Base Agent'

    def run(self, input: AnalysisInput) -> AgentOutput:
        raise NotImplementedError

    # ---- helpers ----

    def stable_score(self, input: AnalysisInput, lo: int = 55, hi: int = 88) -> int:
        """
        Deterministic 0-99 score derived from agent id + key input fields.
        Means: same product + same target market always yields the same score
        for the same agent, but different agents see different scores.
        """
        key = '|'.join([
            self.id,
            input.get('product_name', ''),
            input.get('product_category', ''),
            input.get('target_market', ''),
            input.get('price_tier', ''),
            input.get('brand_goal', ''),
        ])
        digest = hashlib.sha256(key.encode('utf-8')).digest()
        # use first two bytes as 16-bit unsigned and scale into range
        n = (digest[0] << 8) + digest[1]
        span = hi - lo
        return lo + (n % (span + 1))


# Per-target-market context used by multiple agents to ground their mock output.
# Keep entries short — each agent picks the slices it needs.
MARKET_CONTEXT = {
    'Japan': {
        'palette_hint': {
            'primary': '#1A1A1A', 'secondary': '#FAFAF7',
            'accent': '#2C3E50', 'background': '#FAFAFA', 'warning': '#C04040',
        },
        'culture_themes': [
            'Precision and restraint over expressive copy',
            'Quantified ingredient amounts read as trust',
            'Conservative typography signals quality',
            'Pharmacy and convenience-store visual conventions differ sharply',
        ],
        'trust_markers': [
            'Pharmacy-grade seal', 'Third-party verification stamp',
            'Country-of-origin in small kanji', 'Quantified daily dose',
        ],
        'avoid': [
            'Loud Western lifestyle photography',
            'Bold superlative claims ("best", "amazing")',
            'Cluttered front-of-pack hierarchy',
        ],
        'buyer_motivation': 'Trust + functional precision; conservative wellness buyers value verification over aspiration.',
    },
    'South Korea': {
        'palette_hint': {
            'primary': '#0A0A0A', 'secondary': '#FAF7F2',
            'accent': '#4ECDC4', 'background': '#FFFFFF', 'warning': '#D44C4C',
        },
        'culture_themes': [
            'K-Wellness / K-Beauty visual cues',
            'Quantified, specific claims drive D2C trust',
            'Lifestyle wellness over clinical wellness',
            'Influencer-shareability is part of packaging',
        ],
        'trust_markers': [
            'Specific ingredient mg/g amounts', 'Lab-tested seal',
            'D2C reviews count cue', 'Limited-edition / batch language',
        ],
        'avoid': [
            'Clinical pharmacy aesthetic for D2C',
            'Generic Western "wellness" stock photography',
            'Underspecified claims like "supports health"',
        ],
        'buyer_motivation': 'Lifestyle wellness with quantified payoff; buyers expect specificity and shareable design.',
    },
    'Germany': {
        'palette_hint': {
            'primary': '#1A1A1A', 'secondary': '#F5F5F0',
            'accent': '#2E7D32', 'background': '#FFFFFF', 'warning': '#C62828',
        },
        'culture_themes': [
            'Restraint reads as quality',
            'Ingredient transparency is non-negotiable',
            'Sustainability is table-stakes, not a premium',
            'Origin and provenance are strong purchase drivers',
        ],
        'trust_markers': [
            'Full nutrition declaration', 'Organic / Bio certifications',
            'Allergen panel formatted to EU norms', 'Origin country clear',
        ],
        'avoid': [
            'Hype claims and superlatives',
            'Bright fun-pack design at premium price tier',
            'Vague sustainability cues without certification',
        ],
        'buyer_motivation': 'Trust + transparency. Restraint signals quality. Specific provenance and certifications matter more than emotion.',
    },
    'EU': {
        'palette_hint': {
            'primary': '#1A1A1A', 'secondary': '#F5F5F0',
            'accent': '#1E40AF', 'background': '#FFFFFF', 'warning': '#C62828',
        },
        'culture_themes': [
            'EFSA-permitted claim wording is required',
            'Allergen visibility is highly regulated',
            'Cross-border consistency matters more than local flair',
            'Sustainability cues require certification',
        ],
        'trust_markers': [
            'EFSA-compliant claim phrasing', 'Full allergen panel',
            'EU organic logo where applicable', 'Importer / EU distributor field',
        ],
        'avoid': [
            'Disease-risk reduction claims without authorization',
            'Country-specific copy on a pan-EU SKU',
            'Unfounded "natural" or "clean" claims',
        ],
        'buyer_motivation': 'Compliance + trust + restraint. EU shoppers expect formal label structure across the bloc.',
    },
    'Nordics': {
        'palette_hint': {
            'primary': '#1F2937', 'secondary': '#F5F2EC',
            'accent': '#4A5568', 'background': '#FFFFFF', 'warning': '#C24A4A',
        },
        'culture_themes': [
            'Restraint, whitespace, origin-led storytelling',
            'Sustainability, fishery/farm provenance carry weight',
            'Cleaner palettes and lower visual density',
            'Less hype, more documented quality',
        ],
        'trust_markers': [
            'MSC / ASC / origin certifications', 'Quantified ingredient',
            'Cleaner whitespace', 'Verified origin line',
        ],
        'avoid': [
            'US-style hype copy',
            'Bright high-saturation palettes at premium price tier',
            'Generic stock-photo styling',
        ],
        'buyer_motivation': 'Provenance + restraint. Nordic buyers respond to documented sustainability and understated design.',
    },
    'USA': {
        'palette_hint': {
            'primary': '#050505', 'secondary': '#FFFFFF',
            'accent': '#DC2626', 'background': '#FFFFFF', 'warning': '#F59E0B',
        },
        'culture_themes': [
            'Specificity and quantification win',
            'Functional benefit hierarchy first, brand second',
            'FDA-style supplement disclaimers expected',
            'Bold contrast and category-native cues read trustworthy',
        ],
        'trust_markers': [
            'Specific ingredient amounts per serving',
            'Third-party tested seal', 'GMP / NSF / informed-choice logos',
            'FDA disclaimer for supplement claims',
        ],
        'avoid': [
            'Vague functional language',
            'European restraint at mass-market price',
            'Missing supplement disclaimer line',
        ],
        'buyer_motivation': 'Measurable benefit + trust seals. US D2C rewards specificity over subtlety.',
    },
}

# Generic fallback for markets not listed above.
DEFAULT_MARKET_CONTEXT = {
    'palette_hint': {
        'primary': '#0A0A0A', 'secondary': '#F8FAFC',
        'accent': '#7C3AED', 'background': '#FFFFFF', 'warning': '#EF4444',
    },
    'culture_themes': [
        'Lead with quantified benefit',
        'Match local category visual norms',
        'Trust signals tailored to chosen retail channel',
    ],
    'trust_markers': [
        'Quantified ingredient', 'Third-party verification',
        'Origin clarity', 'Channel-appropriate certification',
    ],
    'avoid': [
        'Generic claims without specificity',
        'Mismatch between price tier and palette',
        'Cluttered front-of-pack',
    ],
    'buyer_motivation': 'Lead with quantified benefit and a trust signal appropriate to the channel.',
}


def market_context(target_market: str) -> dict:
    return MARKET_CONTEXT.get(target_market, DEFAULT_MARKET_CONTEXT)
