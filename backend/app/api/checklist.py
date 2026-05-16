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
from ..services.lead_store import add_lead, count_leads

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

    # Local SQLite is the system of record — captures every lead even when
    # Resend is unconfigured or down. Resend is just a downstream fan-out.
    try:
        is_new = add_lead(email=email, company=company, category=category, source='configurator')
    except Exception:
        logger.exception('lead_store.add_lead failed')
        is_new = False

    api_key = os.environ.get('RESEND_API_KEY')
    if not api_key:
        # Lead is in SQLite already — Resend fan-out is just skipped.
        return jsonify({'ok': True, 'captured': True, 'resend_synced': False, 'is_new': is_new}), 200

    audience_id = os.environ.get('RESEND_AUDIENCE_ID')
    if not audience_id:
        return jsonify({'ok': True, 'captured': True, 'resend_synced': False, 'is_new': is_new}), 200

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


def _baseline() -> int:
    """Offline early-tester count added on top of the live Resend audience.
    Configured via BASELINE_LEAD_COUNT env var. Used so the homepage counter
    reflects users we've onboarded outside Resend (Slack groups, manual demos)."""
    try:
        return max(0, int(os.environ.get('BASELINE_LEAD_COUNT', '0') or 0))
    except ValueError:
        return 0


@checklist_bp.route('/count', methods=['GET'])
def lead_count():
    """Return baseline + local store count. Public, cached for 60s."""
    now = time.monotonic()
    baseline = _baseline()

    if (
        _count_cache['count'] is not None
        and (now - _count_cache['ts']) < _COUNT_TTL_SECONDS
    ):
        return jsonify({'count': _count_cache['count'] + baseline, 'cached': True}), 200

    try:
        n = count_leads()
    except Exception as e:
        logger.exception('lead_store.count_leads failed')
        return jsonify({'count': (_count_cache.get('count') or 0) + baseline, 'error': str(e)}), 200

    _count_cache['count'] = n
    _count_cache['ts'] = now
    return jsonify({'count': n + baseline, 'stored': n, 'baseline': baseline}), 200
