"""
Visual style modes and brand types — shared definitions used by the agents
(when shaping the adaptation brief) and the image-generation prompt
(when rendering the label adaptation).

Keeping this in one module means the design direction text, palette
overlays, and style constraints stay in sync across analysis and rendering.
"""

from __future__ import annotations
from typing import TypedDict, List, Optional


class StyleModeSpec(TypedDict, total=False):
    designDirection: str
    styleConstraints: List[str]
    forbiddenStyles: List[str]
    paletteOverlay: dict  # extra palette keys (gradient, metallicAccent)
    promptInstruction: str  # what the image model should do


# --------------------------------------------------------------------------
# Visual style modes
# --------------------------------------------------------------------------

VISUAL_STYLE_MODES: dict = {
    'Clean Premium': {
        'designDirection': (
            'Restrained palette, high whitespace, single hero benefit, quiet confidence, '
            'low visual noise.'
        ),
        'styleConstraints': [
            'High whitespace; minimum 30% negative space around hero benefit',
            'No gradients or glow effects',
            'Single accent color carrying the trust signal',
            'Restrained typography; one display face plus one body face',
        ],
        'forbiddenStyles': [
            'No loud gradients or glow effects',
            'No metallic surfaces',
            'No decorative pattern overlays',
        ],
        'paletteOverlay': {},
        'promptInstruction': (
            'Use restraint, whitespace, clear hierarchy, subtle premium cues. '
            'Avoid loud gradients, heavy effects, and over-decoration.'
        ),
    },
    'Stylish Premium': {
        'designDirection': (
            'Sophisticated gradients, controlled glow, metallic accents, depth, '
            'memorable visual identity. Expressive but commercially credible.'
        ),
        'styleConstraints': [
            'Allow a controlled gradient between primary and accent — no rainbow',
            'Allow one metallic surface cue (foil-stamp / chrome) on a single asset',
            'Maintain a single hero benefit; depth supports it, does not replace it',
            'Restraint in typography even when palette is expressive',
        ],
        'forbiddenStyles': [
            'No childish or chaotic visual treatment',
            'No generic AI-art "neon rainbow" effects',
            'No more than one metallic surface on the label',
        ],
        'paletteOverlay': {
            'gradient': 'primary → accent · controlled, no rainbow',
            'metallicAccent': '#C9A961',  # warm champagne foil-stamp cue
        },
        'promptInstruction': (
            'Use sophisticated gradients, premium glow effects, metallic accents, depth, '
            'and memorable visual cues. The design may feel elevated and expressive, but '
            'must still look commercial and credible. Do not make it childish, chaotic, '
            'or like generic AI art.'
        ),
    },
    'Bold Retail': {
        'designDirection': (
            'Strong contrast, oversized hero benefit, high shelf visibility, direct '
            'benefit hierarchy, immediate product recognition at distance.'
        ),
        'styleConstraints': [
            'High-contrast hero benefit vs. background (4.5:1 minimum)',
            'Bold display typography on the front benefit',
            'Clear product recognition zone (photo or hero illustration)',
            'Direct claim language where regulation allows',
        ],
        'forbiddenStyles': [
            'No high whitespace at the expense of shelf impact',
            'No subtle gradients that disappear on a supermarket shelf',
        ],
        'paletteOverlay': {},
        'promptInstruction': (
            'Use high contrast, strong shelf impact, direct benefit hierarchy, and '
            'clear product recognition. Front benefit must be readable at 1.5m shelf '
            'distance and at thumbnail size.'
        ),
    },
    'Clinical / Scientific': {
        'designDirection': (
            'Precise structure, quantified benefits, technical trust cues, '
            'clean data-led layout.'
        ),
        'styleConstraints': [
            'Quantified hero benefit (mg / g / IU / day-supply)',
            'Mono / technical body typography',
            'Visible third-party-test or lab-tested cue',
            'No lifestyle imagery; allow molecular / capsule / structural cues',
        ],
        'forbiddenStyles': [
            'No emotional / lifestyle photography',
            'No soft pastel palettes',
            'No expressive typography on the benefit line',
        ],
        'paletteOverlay': {},
        'promptInstruction': (
            'Use precise structure, quantified benefit callouts, technical trust cues, '
            'clean data-led layout. Quantify everything that can be quantified.'
        ),
    },
    'Natural / Organic': {
        'designDirection': (
            'Earth tones, ingredient or origin imagery, soft textures, sustainability '
            'and provenance cues.'
        ),
        'styleConstraints': [
            'Earth-tone palette (clay, moss, oat, stone)',
            'Ingredient / botanical illustration or matte texture cue',
            'Origin or sustainability line prominent on front-of-pack',
            'Soft tactile feel — uncoated paper / kraft cue',
        ],
        'forbiddenStyles': [
            'No saturated synthetic palettes (electric pink / cyan)',
            'No heavy gradients or glow effects',
            'No "fake-natural" claims without certification',
        ],
        'paletteOverlay': {},
        'promptInstruction': (
            'Use natural textures, ingredient/origin cues, earthy or soft palettes, '
            'and lower visual aggression. Photographic naturalism over graphic abstraction.'
        ),
    },
    'Luxury Minimal': {
        'designDirection': (
            'Very restrained design, premium material cues, matte finish, metallic '
            'accent, sparse copy.'
        ),
        'styleConstraints': [
            'Sparse copy: no more than 4 elements on front-of-pack',
            'Matte / uncoated finish cue; debossed or foil-stamped accents only',
            'High whitespace; product name in editorial serif',
            'Reserve metallic accent for one mark only',
        ],
        'forbiddenStyles': [
            'No saturated palettes',
            'No photographic hero imagery',
            'No more than one metallic element',
        ],
        'paletteOverlay': {
            'metallicAccent': '#C9A961',
        },
        'promptInstruction': (
            'Use sparse copy, matte feel, high whitespace, restrained typography, and '
            'subtle metallic or embossing cues. Reserve metallic accent for one element.'
        ),
    },
    'Trend-led / D2C': {
        'designDirection': (
            'Modern internet-native look, bold typography, social-friendly packaging, '
            'thumbnail readability.'
        ),
        'styleConstraints': [
            'Hero benefit readable at 200px thumbnail',
            'Modern display typography with personality',
            'Single bold accent color encoding the benefit',
            'Designed for shareability — front-of-pack works in a photo at any angle',
        ],
        'forbiddenStyles': [
            'No traditional pharmacy-style restraint',
            'No cluttered shelf-style hierarchy',
        ],
        'paletteOverlay': {},
        'promptInstruction': (
            'Use modern typography, social-commerce readability, thumbnail clarity, '
            'and energetic but controlled visual cues.'
        ),
    },
    'Keep current brand style': {
        'designDirection': (
            'Preserve the existing visual identity — palette, typography, illustration '
            'style. Improve only hierarchy, wording, market fit, and label clarity.'
        ),
        'styleConstraints': [
            'Preserve the existing palette and typography style',
            'Preserve the existing illustration / photographic treatment',
            'Improve only hierarchy, wording, market fit, and risk areas',
        ],
        'forbiddenStyles': [
            'Do not introduce a new visual identity',
            'Do not recolor signature brand assets',
        ],
        'paletteOverlay': {},
        'promptInstruction': (
            'Preserve the existing visual identity as much as possible. Only improve '
            'hierarchy, wording, market fit, and label clarity. Do not force a new '
            'visual identity.'
        ),
    },
}


# --------------------------------------------------------------------------
# Brand types
# --------------------------------------------------------------------------

BRAND_TYPES: dict = {
    'Own brand': {
        'styleConstraints': [
            'Preserve distinctive brand identity',
            'Allow stronger brand storytelling on front-of-pack',
            'Founder / origin narrative is permitted',
        ],
        'promptInstruction': (
            'Preserve distinctive identity and allow stronger storytelling.'
        ),
    },
    'Private label': {
        'styleConstraints': [
            'Optimize for retailer / distributor credibility',
            'Category-clarity first, founder personality second',
            'Less personality-driven copy',
            'Pricing tier must be unambiguous on shelf',
        ],
        'promptInstruction': (
            'Optimize for retailer / distributor credibility and category clarity. '
            'Less personality-driven; more category-readable.'
        ),
    },
    'White label': {
        'styleConstraints': [
            'Design must be commercially neutral and adaptable',
            'Avoid signature illustration that locks the design to one buyer',
            'Reserve a clear brand-name zone for downstream rebranding',
        ],
        'promptInstruction': (
            'Keep the design adaptable and commercially neutral so multiple buyers '
            'can apply their own brand mark over a clear naming zone.'
        ),
    },
    'Distributor / importer brand': {
        'styleConstraints': [
            'Origin / provenance line must be prominent',
            'Importer / distributor field reserved on front-or-side',
            'Compliance clarity (local-language allergens, ingredient list)',
            'Category explanation for buyers new to the format',
        ],
        'promptInstruction': (
            'Emphasize origin, trust, import clarity, and compliance-readiness. '
            'Category explanation is more important than founder storytelling.'
        ),
    },
    'Retailer brand': {
        'styleConstraints': [
            'Match retailer house design language',
            'Shelf clarity and category consistency over personality',
            'Price-tier cue must align with retailer\'s tiering system',
        ],
        'promptInstruction': (
            'Emphasize shelf clarity, category expectations, and price-tier fit. '
            'Match the retailer\'s broader design language.'
        ),
    },
}


# --------------------------------------------------------------------------
# Lookup helpers (safe defaults when the input is missing or unknown).
# --------------------------------------------------------------------------

def style_mode_spec(name: Optional[str]) -> StyleModeSpec:
    return VISUAL_STYLE_MODES.get(
        (name or '').strip(),
        VISUAL_STYLE_MODES['Keep current brand style'],
    )


def brand_type_spec(name: Optional[str]) -> dict:
    return BRAND_TYPES.get(
        (name or '').strip(),
        BRAND_TYPES['Own brand'],
    )
