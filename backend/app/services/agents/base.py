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
    'Denmark': {
        'palette_hint': {
            'primary': '#1A1A1A', 'secondary': '#F4EFE8',
            'accent': '#B83A2F', 'background': '#FAFAF7', 'warning': '#C24A4A',
        },
        'culture_themes': [
            'Restrained Scandinavian palette with warm cream base',
            'Hygge / quiet quality cues outperform marketing hype',
            'Origin and provenance are explicit purchase drivers',
            'Sustainability is expected, not premium-tier',
        ],
        'trust_markers': [
            'EU Bio / Nyckelhålet label where applicable',
            'Allergen panel in Danish, formatted to FIC norms',
            'Origin badge (Made in Denmark or named EU country)',
            'Single restrained accent color',
        ],
        'avoid': [
            'US-style hype copy and superlatives',
            'Generic stock food photography',
            'Saturated primary colors at premium tier',
        ],
        'buyer_motivation': 'Quiet quality plus documented provenance. Restraint reads premium; loud hype reads cheap.',
    },
    'Norway': {
        'palette_hint': {
            'primary': '#1F2937', 'secondary': '#F8FAFC',
            'accent': '#1B4965', 'background': '#FFFFFF', 'warning': '#C24A4A',
        },
        'culture_themes': [
            'Cool palette: slate, fjord blue, ice white',
            'Norwegian provenance is a premium signal in itself',
            'Sustainability and fishery certifications carry weight',
            'Restrained whitespace, like the broader Nordic tradition',
        ],
        'trust_markers': [
            'Nyt Norge / Made in Norway badge when applicable',
            'MSC / ASC for marine origin',
            'Norwegian-language ingredient list',
            'Restrained whitespace as a trust signal',
        ],
        'avoid': [
            'US-style hype claims and superlatives',
            'Bright saturated palettes at premium price tier',
            'Generic stock-photo styling',
        ],
        'buyer_motivation': 'Norwegian buyers respond to documented origin, sustainability, and restrained design. Cool-palette premium reads well; hype does not.',
    },
    'Sweden': {
        'palette_hint': {
            'primary': '#1A1A1A', 'secondary': '#F5F2EC',
            'accent': '#2C5F2D', 'background': '#FAFAF7', 'warning': '#C24A4A',
        },
        'culture_themes': [
            'Functional design: clean typography over imagery',
            'Plant-forward and organic cues are mainstream, not niche',
            'Bilingual SE / EN front-of-pack is common',
            'Restraint signals quality',
        ],
        'trust_markers': [
            'KRAV / EU Bio / Svanen eco-labels',
            'Nyckelhålet healthier-choice mark when applicable',
            'Swedish-language ingredient list',
            'Origin: Made in Sweden or named EU country',
        ],
        'avoid': [
            'Saturated bold palettes at premium tier',
            'Hyper-cute character mascots on adult food',
            'Hype claims without third-party substantiation',
        ],
        'buyer_motivation': 'Swedish buyers reward restrained, functional, plant-forward design. Eco-labels and Nyckelhålet beat marketing copy.',
    },
    'Lithuania': {
        'palette_hint': {
            'primary': '#1A1A1A', 'secondary': '#F2EBD9',
            'accent': '#B07A2F', 'background': '#FAF7EC', 'warning': '#C24A4A',
        },
        'culture_themes': [
            'Warm Baltic palette: amber, honey, cream',
            'Heritage and tradition cues outperform "modern wellness"',
            'Local references work (rye, honey, dairy, amber)',
            'Bilingual LT / EN is common in premium retail',
        ],
        'trust_markers': [
            'Lithuanian-language ingredient list',
            'Heritage / craft cues if substantiated',
            'Origin: Made in Lithuania or named EU country',
            'EU Bio when applicable',
        ],
        'avoid': [
            'Generic Western stock photography',
            'Hyper-modern minimalism that feels imported',
            'English-only front-of-pack',
        ],
        'buyer_motivation': 'Lithuanian buyers respond to warm-palette heritage cues, local tradition, and clear bilingual labelling. Cold minimalism reads foreign.',
    },
    'United Kingdom': {
        'palette_hint': {
            'primary': '#1A1A1A', 'secondary': '#F2EFE8',
            'accent': '#1F4A2C', 'background': '#FFFFFF', 'warning': '#C62828',
        },
        'culture_themes': [
            'Heritage cues plus clean modern execution',
            'Premium UK supermarket private label sets the bar',
            'Source-traceable provenance carries strong weight',
            'Plain English wins over American hype',
        ],
        'trust_markers': [
            'Red Tractor / Soil Association badge',
            'UK origin or named UK farm / region',
            'Allergen panel formatted to FSA expectations',
            'Plain-English ingredient names',
        ],
        'avoid': [
            'American hype copy and superlatives',
            'Saturated cartoon-style packaging at premium tier',
            'Vague "natural" claims without certification',
        ],
        'buyer_motivation': 'UK buyers reward heritage, traceability, and plain language. Premium reads as restraint plus a single credible trust badge.',
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


# ---------------------------------------------------------------------------
# Hofstede 6D country scores.
# Source: Hofstede Insights public country-comparison tool
# (geerthofstede.com / hofstede-insights.com).
# Dimensions:
#   pdi — Power Distance Index
#   idv — Individualism vs Collectivism
#   mas — Masculinity vs Femininity
#   uai — Uncertainty Avoidance
#   lto — Long-Term Orientation
#   ivr — Indulgence vs Restraint
# Values are 0..100. Missing dimensions are stored as None.
# ---------------------------------------------------------------------------

HOFSTEDE_SCORES: dict = {
    'Japan':          {'pdi': 54, 'idv': 46, 'mas': 95, 'uai': 92, 'lto': 88,  'ivr': 42},
    'South Korea':    {'pdi': 60, 'idv': 18, 'mas': 39, 'uai': 85, 'lto': 100, 'ivr': 29},
    'Germany':        {'pdi': 35, 'idv': 67, 'mas': 66, 'uai': 65, 'lto': 83,  'ivr': 40},
    'USA':            {'pdi': 40, 'idv': 91, 'mas': 62, 'uai': 46, 'lto': 26,  'ivr': 68},
    'United Kingdom': {'pdi': 35, 'idv': 89, 'mas': 66, 'uai': 35, 'lto': 51,  'ivr': 69},
    'Denmark':        {'pdi': 18, 'idv': 74, 'mas': 16, 'uai': 23, 'lto': 35,  'ivr': 70},
    'Norway':         {'pdi': 31, 'idv': 69, 'mas':  8, 'uai': 50, 'lto': 35,  'ivr': 55},
    'Sweden':         {'pdi': 31, 'idv': 71, 'mas':  5, 'uai': 29, 'lto': 53,  'ivr': 78},
    'Lithuania':      {'pdi': 42, 'idv': 60, 'mas': 19, 'uai': 65, 'lto': 82,  'ivr': 16},
    'UAE':            {'pdi': 90, 'idv': 25, 'mas': 50, 'uai': 80, 'lto': None,'ivr': None},
}

# Aggregate buckets that ship with MARKET_CONTEXT but aren't true countries.
HOFSTEDE_SCORES['Nordics'] = {
    'pdi': 27, 'idv': 71, 'mas': 10, 'uai': 38, 'lto': 41, 'ivr': 67,
}
HOFSTEDE_SCORES['EU'] = {
    'pdi': 45, 'idv': 65, 'mas': 45, 'uai': 70, 'lto': 60, 'ivr': 50,
}


def _band(score: Optional[int]) -> str:
    if score is None:
        return 'no published score'
    if score >= 70:
        return 'high'
    if score >= 45:
        return 'mid'
    return 'low'


_HOFSTEDE_GUIDANCE = {
    # (dimension, band) -> short label-design implication
    ('pdi', 'high'): 'Show authority and hierarchy cues — expert endorsements, formal language, status markers.',
    ('pdi', 'mid'):  'Mix expert endorsement with peer reassurance.',
    ('pdi', 'low'):  'Speak peer-to-peer. Avoid status posturing, formal awards, or authority badges as the hero.',
    ('idv', 'high'): "Address the buyer as an individual ('your goal', 'your body'). Personal achievement framing works.",
    ('idv', 'mid'):  'Balance individual and family / shared-meal framing.',
    ('idv', 'low'):  "Lead with shared, family, or in-group language ('for your family', 'made for us').",
    ('mas', 'high'): 'Performance and competition cues work — protein grams, "fuels", achievement frames.',
    ('mas', 'mid'):  'Achievement framing is fine but balance with wellbeing.',
    ('mas', 'low'):  'Lead with care, wellbeing, balance, and quality of life. Avoid competition or "fuel" language.',
    ('uai', 'high'): 'High demand for certifications, ingredient transparency, allergen panels, regulatory marks. Vague claims read as risky.',
    ('uai', 'mid'):  'Standard certifications expected; one strong trust mark beats none.',
    ('uai', 'low'):  'Buyers tolerate ambiguity. A short claim list and one credible mark is enough; over-certification feels cold.',
    ('lto', 'high'): 'Tradition, heritage, "since YYYY", multi-year sustainability stories all carry weight.',
    ('lto', 'mid'):  'Balance heritage cues with present-day relevance.',
    ('lto', 'low'):  'Lead with immediate benefit, novelty, and trend relevance. Heritage framing reads as outdated.',
    ('ivr', 'high'): 'Enjoyment, indulgence, treat-yourself framing fits. Pleasure is a valid hero.',
    ('ivr', 'mid'):  'Treat framing works but only when balanced by a credible benefit.',
    ('ivr', 'low'):  'Restraint, duty, discipline. Pleasure framing feels frivolous. Lead with the functional benefit.',
}


def hofstede_for(target_market: str) -> Optional[dict]:
    """Return raw Hofstede scores for the market, or None if not listed."""
    return HOFSTEDE_SCORES.get(target_market)


def hofstede_summary(target_market: str) -> str:
    """
    Return a prompt-friendly, multi-line summary of Hofstede dimensions and
    the label-design implications. Empty string if the market has no scores.
    """
    scores = HOFSTEDE_SCORES.get(target_market)
    if not scores:
        return ''

    lines = [f'Hofstede 6D scores for {target_market} (Hofstede Insights):']
    name_map = {
        'pdi': 'Power Distance',
        'idv': 'Individualism',
        'mas': 'Masculinity (achievement-orientation)',
        'uai': 'Uncertainty Avoidance',
        'lto': 'Long-Term Orientation',
        'ivr': 'Indulgence',
    }
    for dim in ('pdi', 'idv', 'mas', 'uai', 'lto', 'ivr'):
        score = scores.get(dim)
        band = _band(score)
        score_text = f'{score}' if score is not None else '—'
        guidance = _HOFSTEDE_GUIDANCE.get((dim, band), '')
        lines.append(f'  - {name_map[dim]}: {score_text} ({band}). {guidance}')
    return '\n'.join(lines)
