# Migration script: generate account.move for all eletronic.documents in
# state 'imported' that do not yet have an active (draft/posted) invoice.
# Runs automatically during upgrade to 13.0.1.0.7.
# Re-run after fixing proper account.move instantiation of delivery and
# insurance lines to prevent unbalanced journal entries.

import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info(
        "Starting migration: generating invoices for imported NF-es without an active invoice..."
    )

    env = api.Environment(cr, SUPERUSER_ID, {})

    # All eletronic.documents in 'imported' state
    edocs = env['eletronic.document'].search([('state', '=', 'imported')])

    # Filter: only those without an active account.move (draft or posted)
    edocs_without_invoice = edocs.filtered(
        lambda e: not env['account.move'].search([
            ('eletronic_doc_id', '=', e.id),
            ('state', 'in', ('draft', 'posted')),
        ], limit=1)
    )

    _logger.info(
        "Found %d imported NF-e(s) without an active invoice. Generating...",
        len(edocs_without_invoice),
    )

    success = 0
    errors = 0
    for edoc in edocs_without_invoice:
        try:
            edoc.generate_account_move()
            cr.commit()
            success += 1
            _logger.info(
                "Invoice generated for edoc ID=%s (NF-e %s/%s)",
                edoc.id, edoc.numero, edoc.serie_documento,
            )
        except Exception as e:
            cr.rollback()
            errors += 1
            _logger.warning(
                "Failed to generate invoice for edoc ID=%s (NF-e %s/%s): %s",
                edoc.id, edoc.numero, edoc.serie_documento, str(e),
            )

    _logger.info(
        "Migration finished. Success: %d | Errors: %d",
        success, errors,
    )
