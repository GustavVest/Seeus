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
