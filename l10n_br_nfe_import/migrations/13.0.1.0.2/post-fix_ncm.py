# Script to automatically fix missing NCM in products created from NFe import.
# Runs automatically during module update to version 13.0.1.0.2.

import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    _logger.info("Starting NCM fix for existing products...")
    
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Find all document lines from XML imports that have an NCM and are linked to a product
    lines_with_ncm = env['eletronic.document.line'].search([
        ('product_id', '!=', False),
        ('ncm', '!=', False)
    ])
    
    products_to_fix = {}
    for line in lines_with_ncm:
        if not line.product_id.l10n_br_ncm_id:
            # We keep the object and its associated NCM code from the XML
            products_to_fix[line.product_id.id] = (line.product_id, line.ncm)
            
    _logger.info("Found %d products without NCM but linked to an NFe line with an NCM code.", len(products_to_fix))
    
    updated_count = 0
    for product_id, (product, ncm) in products_to_fix.items():
        ncm_id = env['account.ncm'].search([('code', '=', ncm)], limit=1)
        
        # If not found directly, try the dot-separated format (e.g. 8471.30.12 instead of 84713012)
        if not ncm_id and isinstance(ncm, str) and len(ncm) == 8:
            ncm_formatted = "%s.%s.%s" % (ncm[:4], ncm[4:6], ncm[6:])
            ncm_id = env['account.ncm'].search([('code', '=', ncm_formatted)], limit=1)
            
        if ncm_id:
            product.write({'l10n_br_ncm_id': ncm_id.id})
            updated_count += 1
            _logger.info("Updated product ID %s - %s (%s) with NCM: %s", product.id, product.name, product.default_code, ncm_id.code)
        else:
            _logger.warning("NCM '%s' not found in DB for product %s (%s).", ncm, product.name, product.default_code)
            
    _logger.info("Finished. Successfully updated %d products.", updated_count)
