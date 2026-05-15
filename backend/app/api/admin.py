"""
Admin endpoints (token-guarded).

Currently exposes the captured lead list (Resend Audience contacts) so the
operator can view or download leads without having to log into Resend.

Auth:
    Pass ADMIN_TOKEN either as a header  (X-Admin-Token: <token>)
    or as a query parameter             (?token=<token>).

Env vars consumed:
    ADMIN_TOKEN          — shared secret. If unset, all admin routes
                           return 503 so the endpoint can't be hit by
                           accident before configuration.
    RESEND_API_KEY       — Resend secret key.
    RESEND_AUDIENCE_ID   — Audience UUID to list contacts from.
"""

import csv
import io
import os

from flask import Response, jsonify, request

from . import admin_bp
from ..utils.logger import get_logger

logger = get_logger('seeus.api.admin')


def _require_token() -> bool:
    """Compare the provided token against ADMIN_TOKEN. Returns True if OK."""
    expected = os.environ.get('ADMIN_TOKEN')
    if not expected:
        return False
    provided = request.headers.get('X-Admin-Token') or request.args.get('token')
    return bool(provided) and provided == expected


def _fetch_contacts() -> list[dict]:
    """Fetch all contacts in the configured Resend Audience."""
    import resend
    resend.api_key = os.environ['RESEND_API_KEY']
    audience_id = os.environ['RESEND_AUDIENCE_ID']
    result = resend.Contacts.list({'audience_id': audience_id})

    # The SDK can return either a dict with 'data' or a list directly,
    # depending on version. Normalize to a list of dicts.
    if isinstance(result, dict):
        data = result.get('data') or []
    else:
        data = list(result or [])
    return data


@admin_bp.route('/leads', methods=['GET'])
def list_leads_json():
    """JSON listing of all leads in the Resend audience."""
    if not os.environ.get('ADMIN_TOKEN'):
        return jsonify({'error': 'ADMIN_TOKEN is not configured on the server.'}), 503
    if not _require_token():
        return jsonify({'error': 'Unauthorized. Pass X-Admin-Token header or ?token= query.'}), 401
    if not os.environ.get('RESEND_API_KEY') or not os.environ.get('RESEND_AUDIENCE_ID'):
        return jsonify({'error': 'Resend is not configured on the server.'}), 503

    try:
        data = _fetch_contacts()
    except Exception as e:
        logger.exception('Resend Contacts.list failed')
        return jsonify({'error': f'Resend listing failed: {e}'}), 502

    return jsonify({'count': len(data), 'contacts': data}), 200


@admin_bp.route('/leads.csv', methods=['GET'])
def list_leads_csv():
    """CSV download of all leads. Same auth as /leads."""
    if not os.environ.get('ADMIN_TOKEN'):
        return jsonify({'error': 'ADMIN_TOKEN is not configured on the server.'}), 503
    if not _require_token():
        return jsonify({'error': 'Unauthorized. Pass X-Admin-Token header or ?token= query.'}), 401
    if not os.environ.get('RESEND_API_KEY') or not os.environ.get('RESEND_AUDIENCE_ID'):
        return jsonify({'error': 'Resend is not configured on the server.'}), 503

    try:
        data = _fetch_contacts()
    except Exception as e:
        logger.exception('Resend Contacts.list failed')
        return jsonify({'error': f'Resend listing failed: {e}'}), 502

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(['email', 'first_name', 'last_name', 'created_at', 'unsubscribed'])
    for c in data:
        writer.writerow([
            c.get('email', ''),
            c.get('first_name', '') or '',
            c.get('last_name', '') or '',
            c.get('created_at', '') or '',
            'true' if c.get('unsubscribed') else 'false',
        ])

    return Response(
        buf.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=oramaintel-leads.csv'},
    )
