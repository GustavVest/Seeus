"""
Free checklist subscribe endpoint.

If RESEND_API_KEY is set, sends the label-scoring checklist via email and
(optionally) adds the lead to a Resend Audience. If the key is missing,
the lead is captured to the server log and the frontend gets a success
response so the funnel still appears to work — but the email isn't sent.

Env vars consumed:
    RESEND_API_KEY        — Resend secret key (sk_...)
    RESEND_FROM_ADDRESS   — "Name <email@yourdomain>", defaults to Resend's
                            onboarding sender so first-time setup works
                            without verifying a domain.
    RESEND_AUDIENCE_ID    — optional Audience UUID; if set, the lead is
                            added there for newsletter follow-ups.
"""

import os
import re

from flask import request, jsonify

from . import checklist_bp
from ..utils.logger import get_logger

logger = get_logger('seeus.api.checklist')

_EMAIL_RE = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')

CHECKLIST_SUBJECT = 'Your ORAMA INTEL label scoring checklist'

CHECKLIST_HTML = """<!doctype html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, sans-serif; color: #1F2937; line-height: 1.55; max-width: 640px; margin: 0 auto; padding: 32px;">
  <div style="font-family: 'JetBrains Mono', monospace; letter-spacing: 1.5px; font-size: 11px; color: #7C3AED; text-transform: uppercase; margin-bottom: 8px;">
    ORAMA INTEL · LABEL SCORING CHECKLIST
  </div>
  <h1 style="font-size: 28px; line-height: 1.15; color: #050505; margin: 0 0 16px 0;">
    Score your label before adapting for a new market.
  </h1>
  <p>Use this 10-point checklist to evaluate any product label across three lenses: <strong>shelf clarity</strong>, <strong>market fit</strong>, and <strong>premium positioning</strong>.</p>

  <h2 style="font-size: 16px; color: #050505; margin-top: 28px; margin-bottom: 8px;">Shelf clarity</h2>
  <ol style="padding-left: 20px; margin: 0;">
    <li>Hero benefit readable from 1.5&nbsp;m shelf distance</li>
    <li>Product type / category clear within 1 second</li>
    <li>Single dominant visual element (not three competing)</li>
  </ol>

  <h2 style="font-size: 16px; color: #050505; margin-top: 24px; margin-bottom: 8px;">Market fit</h2>
  <ol start="4" style="padding-left: 20px; margin: 0;">
    <li>Origin / provenance visible (when relevant to the market)</li>
    <li>Trust marker matches the channel (pharmacy vs supermarket vs Amazon)</li>
    <li>Local-language ingredient list present</li>
  </ol>

  <h2 style="font-size: 16px; color: #050505; margin-top: 24px; margin-bottom: 8px;">Premium positioning</h2>
  <ol start="7" style="padding-left: 20px; margin: 0;">
    <li>Typography restrained — one display face plus one body face</li>
    <li>Whitespace ≥ 25 % of front-of-pack</li>
    <li>Color palette ≤ 4 colors, with one carrying the benefit</li>
    <li>Claims wording softened to market-permitted phrasing</li>
  </ol>

  <p style="margin-top: 28px; padding: 16px; background: #F8FAFC; border-left: 3px solid #7C3AED;">
    <strong>Scoring:</strong> rate each item 1–10.<br/>
    Total <strong>below 60</strong> = redesign.<br/>
    Total <strong>60–75</strong> = adapt copy + hierarchy.<br/>
    Total <strong>76+</strong> = market-ready.
  </p>

  <p style="margin-top: 32px; font-size: 14px;">
    When you're ready to adapt a product, run a full market-fit analysis at
    <a href="https://www.oramaintel.com" style="color: #7C3AED;">www.oramaintel.com</a>.
  </p>

  <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 28px 0;"/>
  <p style="font-size: 12px; color: #6B7280;">
    You're receiving this because you requested the free label scoring checklist from ORAMA INTEL.<br/>
    Concept guidance only — verify regulatory wording and claims with appropriate counsel for the target market before commercial use.
  </p>
</body>
</html>
"""


@checklist_bp.route('/subscribe', methods=['POST'])
def subscribe():
    body = request.get_json(silent=True) or {}
    email = (body.get('email') or '').strip().lower()
    company = (body.get('company') or '').strip()
    category = (body.get('category') or '').strip()

    if not email or not _EMAIL_RE.match(email):
        return jsonify({'error': 'Please enter a valid email address.'}), 400

    api_key = os.environ.get('RESEND_API_KEY')
    if not api_key:
        # No provider configured — capture to the log so the lead isn't lost,
        # respond OK so the frontend keeps showing the success state.
        logger.warning(
            'RESEND_API_KEY not set — lead captured locally only: '
            f'email={email} company={company!r} category={category!r}'
        )
        return jsonify({'ok': True, 'delivered': False, 'reason': 'no_provider_configured'}), 200

    try:
        import resend
        resend.api_key = api_key

        from_addr = os.environ.get(
            'RESEND_FROM_ADDRESS',
            'ORAMA INTEL <onboarding@resend.dev>',
        )

        # 1) Send the checklist email to the lead.
        resend.Emails.send({
            'from': from_addr,
            'to': [email],
            'subject': CHECKLIST_SUBJECT,
            'html': CHECKLIST_HTML,
        })

        # 2) Optionally add to a Resend Audience so the lead appears on the
        #    Resend dashboard for future newsletter sends.
        audience_id = os.environ.get('RESEND_AUDIENCE_ID')
        if audience_id:
            try:
                resend.Contacts.create({
                    'audience_id': audience_id,
                    'email': email,
                    'first_name': company or None,
                    'unsubscribed': False,
                })
            except Exception as e:
                # Don't fail the whole request if just the audience-add fails.
                logger.warning(f'Resend audience add failed for {email}: {e}')

        logger.info(f'Checklist sent to {email} (company={company!r} category={category!r})')
        return jsonify({'ok': True, 'delivered': True}), 200

    except Exception as e:
        msg = str(e)
        logger.exception('Resend send failed')
        if 'domain' in msg.lower() and 'verify' in msg.lower():
            return jsonify({
                'error': 'The sending domain isn\'t verified in Resend yet. '
                'Verify your domain or use the default onboarding sender.'
            }), 502
        if 'api key' in msg.lower():
            return jsonify({'error': 'Resend API key is invalid.'}), 401
        return jsonify({'error': f'Email delivery failed: {msg}'}), 502
