"""
Label adaptation API.
Reads an uploaded product label and asks Claude (via OpenAI-compat) to compose
a market-specific adaptation grounded in the actual label content.
"""

import base64
import io
import json
import re

from flask import request, jsonify

from . import label_bp
from ..utils.llm_client import LLMClient
from ..utils.logger import get_logger

logger = get_logger('seeus.api.label')

MAX_FILE_BYTES = 10 * 1024 * 1024  # 10 MB
MAX_IMAGE_DIM = 1500  # cap long edge to keep payload manageable
ALLOWED_EXTS = {'pdf', 'png', 'jpg', 'jpeg', 'webp'}


def _looks_like_pdf(raw: bytes) -> bool:
    return raw[:5] == b'%PDF-'


def _open_as_pdf(raw: bytes):
    """Render first page of a PDF to a PIL image. Raises ValueError on failure."""
    import pymupdf
    from PIL import Image
    try:
        doc = pymupdf.open(stream=raw, filetype='pdf')
    except Exception as e:
        raise ValueError(f"PDF parse failed: {e}") from e
    try:
        if doc.page_count == 0:
            raise ValueError("PDF has no pages.")
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=200)
        return Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
    finally:
        doc.close()


def _open_as_image(raw: bytes):
    """Open raw bytes as a PIL image. Raises ValueError on failure."""
    from PIL import Image, UnidentifiedImageError
    try:
        return Image.open(io.BytesIO(raw)).convert('RGB')
    except UnidentifiedImageError as e:
        raise ValueError("File is not a recognizable image format.") from e


def _load_image_bytes(file_storage):
    """
    Convert any supported upload to PNG bytes (first page if PDF).
    Returns (png_bytes, media_type) or raises ValueError with a clear message.

    Strategy: detect by magic bytes first (filename extensions lie). Try PDF
    when the magic matches; otherwise try as an image. If the magic says PDF
    but parsing fails, retry as image so mislabeled files still work.
    """
    raw = file_storage.read()
    if len(raw) > MAX_FILE_BYTES:
        raise ValueError("File exceeds 10 MB limit.")
    if len(raw) == 0:
        raise ValueError("Empty file.")

    from PIL import Image

    img = None
    last_err = None

    if _looks_like_pdf(raw):
        try:
            img = _open_as_pdf(raw)
        except ValueError as e:
            last_err = e

    if img is None:
        try:
            img = _open_as_image(raw)
        except ValueError as e:
            last_err = e

    if img is None:
        detail = f" ({last_err})" if last_err else ''
        raise ValueError(f"Couldn't read this file as a PDF or image{detail}.")

    # Resize so long edge ≤ MAX_IMAGE_DIM
    w, h = img.size
    longest = max(w, h)
    if longest > MAX_IMAGE_DIM:
        scale = MAX_IMAGE_DIM / longest
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    return buf.getvalue(), 'image/png'


def _build_prompt(category, country):
    return f"""You are an expert in packaging design and market-fit analysis for {category} products entering {country}.

The user has attached their current product label image. Look at it carefully — what it says, the visual hierarchy, the palette, the claim style, the trust markers, and the cultural cues.

Propose a market-specific adaptation for the {country} market. Be concrete and grounded in what is actually on the label — do not invent ingredients or claims that aren't there.

Return STRICTLY a single JSON object matching this schema (no commentary, no markdown fences):

{{
  "headline": "Optimized headline, 4-8 words, single line",
  "subline": "Supporting line under the headline, 4-12 words",
  "claim": "One-sentence hero claim that fits this market's buying psychology",
  "palette": [
    {{"name": "Short color name", "hex": "#XXXXXX"}},
    {{"name": "...", "hex": "#XXXXXX"}},
    {{"name": "...", "hex": "#XXXXXX"}},
    {{"name": "...", "hex": "#XXXXXX"}}
  ],
  "hierarchy": [
    "Top-most label element (most prominent)",
    "Second element",
    "Third element",
    "Fourth element",
    "Bottom-most element"
  ],
  "note": "One sentence on the strategic shift this adaptation represents for {country}'s {category} category"
}}

Constraints:
- Exactly 4 palette entries, each with a valid 6-character hex color
- Exactly 5 hierarchy entries, ordered top to bottom of the label
- All keys present, no extras
- Output the JSON object only — no preamble, no markdown
"""


def _parse_json_response(content):
    """Strip markdown fences and parse JSON. Raises ValueError on failure."""
    cleaned = content.strip()
    cleaned = re.sub(r'^```(?:json)?\s*\n?', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\n?```\s*$', '', cleaned)
    cleaned = cleaned.strip()
    # Find first { and last } in case model added stray text
    start = cleaned.find('{')
    end = cleaned.rfind('}')
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start:end + 1]
    return json.loads(cleaned)


def _validate_adaptation(data):
    required = ['headline', 'subline', 'claim', 'palette', 'hierarchy', 'note']
    for k in required:
        if k not in data:
            raise ValueError(f"Missing field: {k}")
    if not isinstance(data['palette'], list) or len(data['palette']) < 1:
        raise ValueError("palette must be a non-empty list")
    for entry in data['palette']:
        if not isinstance(entry, dict) or 'name' not in entry or 'hex' not in entry:
            raise ValueError("palette entries must have name + hex")
    if not isinstance(data['hierarchy'], list) or len(data['hierarchy']) < 1:
        raise ValueError("hierarchy must be a non-empty list")
    return data


@label_bp.route('/debug/keys', methods=['GET'])
def debug_keys():
    """
    Returns metadata about which API keys the running container can see.
    Never exposes the actual secret values — only length + prefix + suffix
    so we can verify Railway stored the right thing. Safe to leave on
    while we're diagnosing env var issues.
    """
    import os

    def describe(value):
        if not value:
            return {'set': False}
        return {
            'set': True,
            'length': len(value),
            'prefix': value[:12],
            'suffix': value[-6:],
        }

    return jsonify({
        'OPENAI_API_KEY': describe(os.environ.get('OPENAI_API_KEY')),
        'LLM_API_KEY':    describe(os.environ.get('LLM_API_KEY')),
        'LLM_BASE_URL':   os.environ.get('LLM_BASE_URL') or None,
        'LLM_MODEL_NAME': os.environ.get('LLM_MODEL_NAME') or None,
    }), 200


@label_bp.route('/adapt', methods=['POST'])
def adapt_label():
    """
    Compose a market-specific adaptation for an uploaded label.

    Request (multipart/form-data):
        file: PDF/PNG/JPG/WEBP of the current label
        category: product category (Food / Beverage / Supplement / Private Label)
        country: target country

    Response (200):
        {
            "headline": "...",
            "subline": "...",
            "claim": "...",
            "palette": [{"name": "...", "hex": "..."}, ...],
            "hierarchy": ["...", ...],
            "note": "..."
        }
    """
    if 'file' not in request.files:
        return jsonify({'error': 'Missing file field'}), 400
    f = request.files['file']
    category = (request.form.get('category') or '').strip()
    country = (request.form.get('country') or '').strip()
    if not category or not country:
        return jsonify({'error': 'category and country are required'}), 400

    try:
        png_bytes, media_type = _load_image_bytes(f)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.exception("Failed to load uploaded label")
        return jsonify({'error': f'Failed to read file: {e}'}), 400

    b64 = base64.b64encode(png_bytes).decode('ascii')
    data_url = f"data:{media_type};base64,{b64}"
    prompt = _build_prompt(category, country)

    messages = [
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': prompt},
                {'type': 'image_url', 'image_url': {'url': data_url}},
            ],
        }
    ]

    try:
        client = LLMClient()
        raw = client.chat(messages=messages, temperature=0.4, max_tokens=2000)
        data = _parse_json_response(raw)
        data = _validate_adaptation(data)
        return jsonify(data), 200
    except json.JSONDecodeError as e:
        logger.error("Claude returned non-JSON content: %s", raw[:500] if 'raw' in dir() else '')
        return jsonify({'error': 'Model returned invalid JSON', 'detail': str(e)}), 502
    except ValueError as e:
        return jsonify({'error': 'Validation failed', 'detail': str(e)}), 502
    except Exception as e:
        msg = str(e)
        logger.exception("Adaptation call failed")
        # Surface common, actionable upstream errors to the user
        if 'credit balance is too low' in msg.lower():
            return jsonify({'error': 'Anthropic API has no credits — add some at console.anthropic.com/settings/billing'}), 402
        if 'invalid x-api-key' in msg.lower() or 'authentication' in msg.lower():
            return jsonify({'error': 'Anthropic API key is invalid or rotated'}), 401
        if 'rate' in msg.lower() and 'limit' in msg.lower():
            return jsonify({'error': 'Anthropic API rate-limited — try again in a moment'}), 429
        return jsonify({'error': f'Adaptation failed: {msg}'}), 500


# ==========================================================================
# /api/label/analyze — full 8-agent market-fit report
# ==========================================================================


def _split_csv(raw):
    """Split a comma/newline-separated string into a clean list."""
    if not raw:
        return []
    parts = re.split(r'[,\n;]', raw)
    return [p.strip() for p in parts if p and p.strip()]


@label_bp.route('/analyze', methods=['POST'])
def analyze_label():
    """
    Run the full 8-agent market-fit analysis.

    Request (multipart/form-data):
        file:             PDF/PNG/JPG/WEBP of the current label (optional in scaffold mode)
        product_name:     str
        product_category: 'Food' | 'Beverage' | 'Supplement' | 'Private Label'
        current_market:   str   (country)
        target_market:    str   (country)
        target_channel:   'supermarket' | 'pharmacy' | 'convenience' | 'amazon' | 'specialty' | 'b2b'
        target_buyer:     str
        price_tier:       'budget' | 'mainstream' | 'premium' | 'luxury'
        brand_goal:       str
        ingredients:      comma/newline-separated string (optional)
        claims_on_pack:   comma/newline-separated string (optional)
        country_of_origin: str (optional)

    Response (200): FinalReport JSON. See agents/types.py.
    """
    # Late import so the agents module is loaded after Flask app is set up.
    from ..services.agents import MarketFitOrchestrator

    form = request.form
    files = request.files

    front_b64 = None
    if 'file' in files and files['file'].filename:
        try:
            png_bytes, _ = _load_image_bytes(files['file'])
            front_b64 = base64.b64encode(png_bytes).decode('ascii')
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.exception("Failed to load uploaded label")
            return jsonify({'error': f'Failed to read file: {e}'}), 400

    back_b64 = None
    if 'back_file' in files and files['back_file'].filename:
        try:
            png_bytes, _ = _load_image_bytes(files['back_file'])
            back_b64 = base64.b64encode(png_bytes).decode('ascii')
        except Exception:
            logger.warning("Failed to load back-label file; continuing without it.")

    analysis_input = {
        'front_label_b64': front_b64,
        'back_label_b64': back_b64,
        'product_name': (form.get('product_name') or '').strip(),
        'product_category': (form.get('product_category') or '').strip(),
        'brand_type': (form.get('brand_type') or 'Own brand').strip(),
        'visual_style_mode': (form.get('visual_style_mode') or 'Keep current brand style').strip(),
        'ingredients': _split_csv(form.get('ingredients')),
        'claims_on_pack': _split_csv(form.get('claims_on_pack')),
        'country_of_origin': (form.get('country_of_origin') or '').strip(),
        'current_market': (form.get('current_market') or '').strip(),
        'target_market': (form.get('target_market') or '').strip(),
        'target_channel': (form.get('target_channel') or 'supermarket').strip(),
        'target_buyer': (form.get('target_buyer') or 'mass').strip(),
        'price_tier': (form.get('price_tier') or 'mainstream').strip(),
        'brand_goal': (form.get('brand_goal') or 'trust').strip(),
    }

    if not analysis_input['target_market']:
        return jsonify({'error': 'target_market is required'}), 400
    if not analysis_input['product_category']:
        return jsonify({'error': 'product_category is required'}), 400

    try:
        report = MarketFitOrchestrator().analyze(analysis_input)
    except Exception as e:
        logger.exception("Orchestrator failed")
        return jsonify({'error': f'Analysis failed: {e}'}), 500

    # Strip the heavy per-agent raw payloads from the public response by
    # default (still available via agentOutputs if explicitly asked).
    if form.get('include_agent_outputs') != '1':
        report = {k: v for k, v in report.items() if k != 'agentOutputs'}

    return jsonify(report), 200


# ==========================================================================
# /api/label/generate-mockup — paid: OpenAI image generation from brief
# ==========================================================================


def _build_label_only_mockup_prompt(brief: dict) -> str:
    """
    Strict label-only adaptation prompt.

    Preserves the original packaging format (shape, casing, cap, perspective,
    lighting) and only changes the printed label artwork.

    Note: even with image-editing, gpt-image-1 can still drift on details.
    The most reliable production system is:
        Claude adaptation brief -> fixed package template -> label artwork
        layer replacement (e.g. Sharp / Pillow composite onto a known mockup).
    """
    palette = brief.get('palette') or {}
    must_preserve = '\n'.join(brief.get('mustPreserve') or [])
    claims_to_avoid = '\n'.join(brief.get('claimsToAvoid') or [])
    safer_claims = '\n'.join(brief.get('saferClaims') or [])
    hierarchy = '\n'.join(brief.get('hierarchy') or [])
    style_constraints = '\n'.join(brief.get('styleConstraints') or [])
    forbidden_changes = '\n'.join(brief.get('forbiddenChanges') or [])

    brand_assets = brief.get('brandAssetsToPreserve') or []
    if brand_assets:
        brand_assets_block = '\n'.join([f'  - {a}' for a in brand_assets])
    else:
        brand_assets_block = (
            '  - Infer the visible brand assets from the uploaded image and preserve them.\n'
            '  - Use the uploaded image as the source of truth.'
        )

    package_type_line = brief.get('packageType') or (
        'Use the uploaded image as the source of truth. Preserve it exactly.'
    )

    refs = brief.get('marketReferenceInsights') or {}
    category_norms = '\n'.join(refs.get('categoryNorms') or []) or '  (none provided)'
    trust_markers_block = '\n'.join(refs.get('trustMarkersToConsider') or []) or '  (none provided)'
    visual_patterns = '\n'.join(refs.get('visualPatternsToRespect') or []) or '  (none provided)'
    patterns_to_avoid = '\n'.join(refs.get('patternsToAvoid') or []) or '  (none provided)'
    diff_ops = '\n'.join(refs.get('differentiationOpportunities') or []) or '  (none provided)'
    retail_expectations = '\n'.join(refs.get('retailChannelExpectations') or []) or '  (none provided)'

    # Visual style mode + brand type — lookup the rules so the prompt is
    # the single source of truth for "what mode means".
    from ..services.agents.style_modes import style_mode_spec, brand_type_spec
    style_mode_name = brief.get('visualStyleMode') or 'Keep current brand style'
    brand_type_name = brief.get('brandType') or 'Own brand'
    style_spec = style_mode_spec(style_mode_name)
    brand_spec = brand_type_spec(brand_type_name)
    style_instruction = style_spec.get('promptInstruction', '')
    brand_instruction = brand_spec.get('promptInstruction', '')
    palette_extras = []
    if palette.get('gradient'):
        palette_extras.append(f"Gradient cue: {palette['gradient']}")
    if palette.get('metallicAccent'):
        palette_extras.append(f"Metallic accent: {palette['metallicAccent']}")
    palette_extras_block = '\n'.join(palette_extras) if palette_extras else ''

    # Recommended label copy surfaced from the analysis report.
    rec_copy = brief.get('recommendedLabelCopy') or {}
    front_headline = (rec_copy.get('frontLabelHeadline') or '').strip() or '(none provided — keep the existing headline)'
    subheadline = (rec_copy.get('subheadline') or '').strip() or '(none provided)'
    benefit_bullets_block = '\n'.join([f'  - {b}' for b in (rec_copy.get('benefitBullets') or [])]) or '  (none provided)'

    return f"""SYSTEM PRINCIPLE:
This is not free creative redesign. This is controlled commercial label adaptation.

You are editing a real product packaging image — creating a market-adapted label concept.

CRITICAL INSTRUCTION:
Preserve the original uploaded product packaging exactly.
Change ONLY the visible printed label artwork.

Do NOT change:
- package shape
- box, bottle, pouch, jar, can, tube, bag, casing, or container
- cap, lid, seal, closure, nozzle, or physical parts
- material, surface, lighting, camera angle, perspective, shadows, or proportions
- product size or packaging format
- background unless unavoidable
- barcode placement if visible
- mandatory information placement unless the brief says otherwise

Only adapt:
- label artwork
- label copy
- front label hierarchy
- color palette (label artwork only — do not recolor the brand logo)
- typography style around non-logo text
- claim wording
- benefit emphasis
- trust markers
- cultural and market-specific visual cues
- shelf-facing communication

==================================================
CRITICAL BRAND PRESERVATION RULE  (overrides all other instructions)
==================================================
The adaptation must keep all distinctive brand assets from the uploaded label.

PRESERVE: Logo, brand name, icon marks, symbols, mascots, emblems, certification marks already present, origin marks already present, signature illustrations, unique brand patterns, characteristic shapes, brand-owned color accents where possible, product name, recognizable visual identity.

DO NOT: replace the logo, invent a new logo, remove brand symbols, change the brand name, add fake certifications, add fake awards, add fake regulatory marks, replace special company elements with generic icons, make the product look like a different company.

BRAND ASSETS TO PRESERVE:
{brand_assets_block}

If there is a conflict between adaptation and brand preservation, BRAND PRESERVATION WINS.
==================================================

Product:
{brief.get('productName', '')}

Category:
{brief.get('category', '')}

Target market:
{brief.get('targetMarket', '')}

Package type to preserve:
{package_type_line}

Must preserve (product facts):
{must_preserve}

Claims to avoid:
{claims_to_avoid}

Safer claims to use:
{safer_claims}

==================================================
RECOMMENDED LABEL COPY  (apply these to the front of the label)
==================================================
Headline:
{front_headline}

Subheadline:
{subheadline}

Benefit bullets:
{benefit_bullets_block}
==================================================

Recommended palette (label artwork only — do not recolor the brand logo):
Primary:    {palette.get('primary', '')}
Secondary:  {palette.get('secondary', '')}
Accent:     {palette.get('accent', '')}
Background: {palette.get('background', '')}
{palette_extras_block}

==================================================
VISUAL STYLE MODE: {style_mode_name}
==================================================
{style_instruction}

BRAND TYPE: {brand_type_name}
{brand_instruction}
==================================================

Design direction:
{brief.get('designDirection', '')}

Recommended hierarchy (top to bottom on the label):
{hierarchy}

Style constraints:
{style_constraints}

Forbidden changes:
{forbidden_changes}

==================================================
MARKET REFERENCE INSIGHTS  (directional context — DO NOT copy any specific competitor label)
==================================================
Category norms:
{category_norms}

Trust markers to consider:
{trust_markers_block}

Visual patterns to respect:
{visual_patterns}

Patterns to avoid (overused clichés in this market):
{patterns_to_avoid}

Differentiation opportunities (white-space):
{diff_ops}

Retail / channel expectations:
{retail_expectations}

CRITICAL: Use the above market references as directional context only.
Do not copy, imitate, or recreate any existing competitor label.
Preserve the uploaded brand identity and packaging shape.
==================================================

Output:
Create a realistic commercial label adaptation concept for the target market.
The final image must look like the SAME PRODUCT and SAME PACKAGE, with an improved localized LABEL.
Do not invent certifications, medical claims, awards, ingredients, or regulatory marks.
Do not add random text.
Avoid unreadable nonsense text.
If exact small text cannot be rendered, use clean placeholder microtext blocks instead of fake words.

This is an AI-generated label adaptation concept, not a final print-ready file.
"""


def _build_mockup_prompt(brief: dict, with_source_image: bool = False) -> str:
    """Compose an OpenAI image-gen prompt from the adaptation brief.

    If with_source_image=True, the prompt is shaped for the image-edit
    endpoint and explicitly tells the model to preserve the package format
    AND the brand assets shown in the input image. Brand preservation wins
    over adaptation in any conflict.
    """
    palette = brief.get('palette') or {}
    hex_summary = ' / '.join([f"{k}: {v}" for k, v in palette.items() if v])
    hierarchy = '\n'.join([f'  {i+1}. {h}' for i, h in enumerate(brief.get('hierarchy') or [])])
    must_preserve = '\n'.join([f'  - {p}' for p in (brief.get('mustPreserve') or [])])
    safer_claims = ', '.join((brief.get('saferClaims') or [])[:3])
    style = ' · '.join(brief.get('styleConstraints') or [])
    forbidden = '\n'.join([f'  - {f}' for f in (brief.get('forbiddenChanges') or [])])

    brand_assets = brief.get('brandAssetsToPreserve') or []
    if brand_assets:
        brand_assets_block = '\n'.join([f'  - {a}' for a in brand_assets])
    else:
        brand_assets_block = (
            '  - Infer the visible brand assets from the uploaded image and preserve them.\n'
            '  - Use the uploaded image as the source of truth for what the brand looks like.'
        )

    source_lead = ''
    if with_source_image:
        source_lead = (
            "The attached image is the CURRENT product packaging. "
            "Redesign the LABEL ARTWORK for the target market below, but PRESERVE the "
            "physical package format shown in the image (cup, can, bottle, pouch, sachet, "
            "box, etc.), its proportions, and its camera angle. Do not change the package "
            "type into a different format. Render the same package shape with new label artwork.\n\n"
        )

    package_type_line = (
        brief.get('packageType') or 'match the package format shown in the source image'
        if with_source_image
        else (brief.get('packageType') or 'standard retail package for the category')
    )

    return f"""{source_lead}Create a realistic market-adapted label concept.
It must look like the SAME COMPANY, SAME PRODUCT, and SAME PACKAGING FORMAT — only improved for the selected market.
Preserve the original brand identity while adapting the label communication.

==================================================
CRITICAL BRAND PRESERVATION RULE  (overrides all other instructions)
==================================================
The adaptation must keep all distinctive brand assets from the uploaded label unless explicitly instructed otherwise.

PRESERVE:
  - Logo
  - Brand name
  - Icon marks
  - Symbols
  - Mascots
  - Emblems
  - Certification marks, if already present on the original
  - Origin marks already present on the original
  - Signature illustrations
  - Unique brand patterns
  - Characteristic shapes
  - Brand-owned color accents where possible
  - Product name (unless the user requests localization)
  - Recognizable visual identity

DO NOT:
  - Replace the logo
  - Invent a new logo
  - Remove brand symbols
  - Change the brand name
  - Add fake certifications
  - Add fake awards
  - Add fake regulatory marks
  - Replace special company elements with generic icons
  - Make the product look like a different company

ONLY ADAPT:
  - label hierarchy
  - supporting copy
  - color balance
  - market-specific emphasis
  - typography around non-logo text
  - claim wording
  - benefit framing
  - layout organization
  - shelf communication

BRAND ASSETS TO PRESERVE:
{brand_assets_block}

If there is a conflict between adaptation and brand preservation, BRAND PRESERVATION WINS.
==================================================

Target market: {brief.get('targetMarket', '')}
Product: {brief.get('productName', '')}  ({brief.get('category', '')})
Package type: {package_type_line}

Visual hierarchy (top to bottom on front-of-pack):
{hierarchy}

Palette balance to lean toward ({hex_summary}) — but DO NOT override the brand's own colors on the logo or signature illustrations:

Must preserve (product facts):
{must_preserve}

Style: {style}.
Design direction: {brief.get('designDirection', '')}.
Safer claim phrasing if any claim is shown: {safer_claims}.

Hard constraints:
{forbidden}

Output: a single high-quality concept mockup image, photographed studio-style on a neutral background, no text on the background, no watermarks. Frame as a packaging concept, not final compliant artwork. Realistic, commercial, export-ready feel.
"""


@label_bp.route('/generate-mockup', methods=['POST'])
def generate_mockup():
    """
    Generate a market-adapted packaging mockup image from an adaptation brief.

    Request (JSON):
        {
            "brief": { ... AdaptationBrief shape from /analyze ... }
        }

    Behavior:
        - If OPENAI_API_KEY is set, call OpenAI image generation.
        - If not, return a deterministic mock placeholder so the UI can still demo.

    Response (200):
        {
            "image_b64": "<base64-encoded PNG>",
            "prompt": "<the composed prompt used>",
            "mock": true|false
        }
    """
    import os
    from PIL import Image, ImageDraw

    # Accept either:
    #   multipart/form-data: brief=<json>, file=<source image>, label_only_mode=<0|1>
    #   application/json:    {"brief": {...}, "labelOnlyMode": true}
    source_image_bytes = None
    label_only_mode = True  # default ON — safer for label adaptation
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        raw_brief = request.form.get('brief') or '{}'
        try:
            brief = json.loads(raw_brief)
        except json.JSONDecodeError:
            return jsonify({'error': 'invalid brief JSON'}), 400
        if 'file' in request.files and request.files['file'].filename:
            try:
                source_image_bytes, _ = _load_image_bytes(request.files['file'])
            except Exception:
                logger.warning("Could not read source image for mockup; falling back to text-only.")
                source_image_bytes = None
        raw_flag = request.form.get('label_only_mode')
        if raw_flag is not None:
            label_only_mode = raw_flag.lower() in ('1', 'true', 'yes', 'on')
    else:
        body = request.get_json(silent=True) or {}
        brief = body.get('brief') or {}
        if 'labelOnlyMode' in body:
            label_only_mode = bool(body['labelOnlyMode'])

    if not brief:
        return jsonify({'error': 'brief is required'}), 400

    # NOTE: For maximum control over "label-only" output, the most reliable
    # system is a fixed package template + a designer/Pillow-composited label
    # artwork layer. Image-edit is the next-best automated path and what we
    # use here. Text-only generation is the weakest fallback.
    if label_only_mode:
        prompt = _build_label_only_mockup_prompt(brief)
    else:
        prompt = _build_mockup_prompt(brief, with_source_image=source_image_bytes is not None)

    api_key = os.environ.get('OPENAI_API_KEY')

    # ---- Mock fallback: render a styled placeholder card so the UI still works.
    def render_mock_placeholder():
        palette = brief.get('palette') or {}
        bg = palette.get('background') or '#F8FAFC'
        primary = palette.get('primary') or '#050505'
        accent = palette.get('accent') or '#7C3AED'

        W, H = 1024, 1024
        img = Image.new('RGB', (W, H), bg)
        d = ImageDraw.Draw(img)
        # Outer card
        d.rectangle((80, 80, W - 80, H - 80), outline=primary, width=3)
        # Color stripe at the top
        d.rectangle((80, 80, W - 80, 200), fill=accent)
        # Hero label area
        d.rectangle((140, 280, W - 140, 700), outline=primary, width=2)
        # Footer
        d.rectangle((140, 780, W - 140, 880), outline=primary, width=2)

        # text via PIL default font (no external font dep)
        try:
            from PIL import ImageFont
            font = ImageFont.load_default()
        except Exception:
            font = None
        text_lines = [
            f"CONCEPT MOCKUP  ·  {brief.get('targetMarket', '').upper()}",
            f"{brief.get('productName', '')}",
            f"{brief.get('category', '')}",
            "[ mock placeholder — set OPENAI_API_KEY to render with AI ]",
        ]
        y = 320
        for line in text_lines:
            d.text((180, y), line, fill=primary, font=font)
            y += 60

        buf = io.BytesIO()
        img.save(buf, format='PNG', optimize=True)
        return base64.b64encode(buf.getvalue()).decode('ascii')

    if not api_key:
        return jsonify({
            'image_b64': render_mock_placeholder(),
            'prompt': prompt,
            'mock': True,
        }), 200

    # ---- Real OpenAI call.
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        if source_image_bytes is not None:
            # Image-edit path: preserves the physical package format from the source.
            buf = io.BytesIO(source_image_bytes)
            buf.name = 'source.png'  # OpenAI SDK uses the filename to infer mime
            resp = client.images.edit(
                model='gpt-image-1',
                image=buf,
                prompt=prompt,
                size='1024x1024',
                n=1,
            )
        else:
            resp = client.images.generate(
                model='gpt-image-1',
                prompt=prompt,
                size='1024x1024',
                n=1,
            )

        b64 = resp.data[0].b64_json
        if not b64 and getattr(resp.data[0], 'url', None):
            # Older response shapes returned a URL; fetch and re-encode.
            import urllib.request
            with urllib.request.urlopen(resp.data[0].url) as r:
                b64 = base64.b64encode(r.read()).decode('ascii')
        if not b64:
            raise RuntimeError('OpenAI returned no image payload')
        return jsonify({
            'image_b64': b64,
            'prompt': prompt,
            'mock': False,
            'mode': 'edit' if source_image_bytes is not None else 'generate',
            'label_only_mode': label_only_mode,
        }), 200
    except Exception as e:
        msg = str(e)
        logger.exception("OpenAI image generation failed")
        msg_low = msg.lower()
        if 'billing_hard_limit' in msg_low or 'billing hard limit' in msg_low:
            user_msg = (
                'OpenAI billing limit reached — raise the monthly cap at '
                'platform.openai.com/settings/organization/limits'
            )
        elif 'insufficient_quota' in msg_low or 'insufficient' in msg_low or 'quota' in msg_low:
            user_msg = 'OpenAI account has no credits — add funds at platform.openai.com/settings/organization/billing'
        elif 'billing' in msg_low:
            user_msg = 'OpenAI billing not configured — check platform.openai.com/settings/organization/billing'
        elif 'invalid api key' in msg_low or 'incorrect api key' in msg_low:
            user_msg = 'OpenAI API key is invalid or rotated'
        elif 'rate limit' in msg_low or 'rate_limit' in msg_low:
            user_msg = 'OpenAI rate-limited — try again in a moment'
        else:
            user_msg = f'Image generation failed: {msg}'
        return jsonify({
            'image_b64': render_mock_placeholder(),
            'prompt': prompt,
            'mock': True,
            'error': user_msg,
        }), 200
