"""
Lead capture endpoint.

Captures the visitor's email + optional company + optional category to a
Resend Audience for follow-up by sales. No transactional email is sent
from this endpoint — we are a lead-list, not a newsletter sender.

Env vars consumed:
    RESEND_API_KEY        — Resend secret key (re_...)
    RESEND_AUDIENCE_ID    — Audience UUID to add the lead to.
                            If unset, the lead is still captured to the
                            backend log so it isn't lost.
"""

import os
import re
import time

from flask import request, jsonify

from . import checklist_bp
from ..utils.logger import get_logger

logger = get_logger('seeus.api.checklist')

_EMAIL_RE = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')

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
        # No provider configured — capture to the log so the lead isn't lost.
        logger.warning(
            'RESEND_API_KEY not set — lead captured locally only: '
            f'email={email} company={company!r} category={category!r}'
        )
        return jsonify({'ok': True, 'captured': False, 'reason': 'no_provider_configured'}), 200

    audience_id = os.environ.get('RESEND_AUDIENCE_ID')
    if not audience_id:
        logger.warning(
            'RESEND_AUDIENCE_ID not set — lead captured locally only: '
            f'email={email} company={company!r} category={category!r}'
        )
        return jsonify({'ok': True, 'captured': False, 'reason': 'no_audience_configured'}), 200

    try:
        import resend
        resend.api_key = api_key

        # Add the lead to the Resend Audience. NO email is sent — we use
        # Resend purely as a contact-list backend.
        resend.Contacts.create({
            'audience_id': audience_id,
            'email': email,
            'first_name': company or None,
            'unsubscribed': False,
        })

        logger.info(f'Lead captured: {email} (company={company!r} category={category!r})')
        return jsonify({'ok': True, 'captured': True}), 200

    except Exception as e:
        msg = str(e)
        logger.exception('Resend contact-add failed')
        if 'api key' in msg.lower():
            return jsonify({'error': 'Resend API key is invalid.'}), 401
        if 'duplicate' in msg.lower() or 'already' in msg.lower():
            # Treat duplicates as success — the lead is already on the list.
            return jsonify({'ok': True, 'captured': True, 'note': 'already_on_list'}), 200
        return jsonify({'error': f'Lead capture failed: {msg}'}), 502


# ---------------------------------------------------------------------------
# Public lead-count for the homepage stat strip.
# Cached in-process for 60s so we don't hit the Resend API on every page load.
# ---------------------------------------------------------------------------

_count_cache = {'count': None, 'ts': 0.0}
_COUNT_TTL_SECONDS = 60.0


@checklist_bp.route('/count', methods=['GET'])
def lead_count():
    """Return the current number of captured leads. Public, cached, safe to embed."""
    now = time.monotonic()
    if (
        _count_cache['count'] is not None
        and (now - _count_cache['ts']) < _COUNT_TTL_SECONDS
    ):
        return jsonify({'count': _count_cache['count'], 'cached': True}), 200

    api_key = os.environ.get('RESEND_API_KEY')
    audience_id = os.environ.get('RESEND_AUDIENCE_ID')
    if not api_key or not audience_id:
        # Resend not configured — return 0 so the frontend can hide the counter
        # gracefully until it's wired up.
        return jsonify({'count': 0, 'configured': False}), 200

    try:
        import resend
        resend.api_key = api_key
        result = resend.Contacts.list({'audience_id': audience_id})
        data = result.get('data') if isinstance(result, dict) else list(result or [])
        n = len(data or [])

        _count_cache['count'] = n
        _count_cache['ts'] = now
        return jsonify({'count': n, 'configured': True}), 200
    except Exception as e:
        logger.exception('Resend count failed')
        # Don't blow up the homepage just because Resend is having a moment.
        return jsonify({'count': _count_cache.get('count') or 0, 'configured': True, 'error': str(e)}), 200
