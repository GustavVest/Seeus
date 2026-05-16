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
from ..services.lead_store import list_leads

logger = get_logger('seeus.api.admin')


def _require_token() -> bool:
    """Compare the provided token against ADMIN_TOKEN. Returns True if OK."""
    expected = os.environ.get('ADMIN_TOKEN')
    if not expected:
        return False
    provided = request.headers.get('X-Admin-Token') or request.args.get('token')
    return bool(provided) and provided == expected


@admin_bp.route('/leads', methods=['GET'])
def list_leads_json():
    """JSON listing of all leads in the local SQLite store."""
    if not os.environ.get('ADMIN_TOKEN'):
        return jsonify({'error': 'ADMIN_TOKEN is not configured on the server.'}), 503
    if not _require_token():
        return jsonify({'error': 'Unauthorized. Pass X-Admin-Token header or ?token= query.'}), 401

    try:
        data = list_leads()
    except Exception as e:
        logger.exception('lead_store.list_leads failed')
        return jsonify({'error': f'Lead listing failed: {e}'}), 502

    return jsonify({'count': len(data), 'leads': data}), 200


@admin_bp.route('/leads.csv', methods=['GET'])
def list_leads_csv():
    """CSV download of all leads from the local SQLite store. Same auth as /leads."""
    if not os.environ.get('ADMIN_TOKEN'):
        return jsonify({'error': 'ADMIN_TOKEN is not configured on the server.'}), 503
    if not _require_token():
        return jsonify({'error': 'Unauthorized. Pass X-Admin-Token header or ?token= query.'}), 401

    try:
        data = list_leads()
    except Exception as e:
        logger.exception('lead_store.list_leads failed')
        return jsonify({'error': f'Lead listing failed: {e}'}), 502

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(['email', 'company', 'category', 'source', 'created_at'])
    for c in data:
        writer.writerow([
            c.get('email', ''),
            c.get('company', '') or '',
            c.get('category', '') or '',
            c.get('source', '') or '',
            c.get('created_at', '') or '',
        ])

    return Response(
        buf.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=oramaintel-leads.csv'},
    )
