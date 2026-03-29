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
        ncm_id = False
        if ncm and ncm != 'None':
            ncm_id = env['account.ncm'].search([('code', '=', ncm)], limit=1)
            
            ncm_digits = ''.join(filter(str.isdigit, str(ncm)))
            if not ncm_id and ncm_digits:
                ncm_id = env['account.ncm'].search([('code', '=', ncm_digits)], limit=1)
                
                if not ncm_id and len(ncm_digits) == 8:
                    ncm_formatted_1 = "%s.%s.%s" % (ncm_digits[:4], ncm_digits[4:6], ncm_digits[6:])
                    ncm_formatted_2 = "%s.%s.%s.%s" % (ncm_digits[:2], ncm_digits[2:4], ncm_digits[4:6], ncm_digits[6:])
                    ncm_id = env['account.ncm'].search([
                        ('code', 'in', [ncm_formatted_1, ncm_formatted_2])
                    ], limit=1)
            
            if not ncm_id and ncm_digits:
                ncm_code = ncm
                if len(ncm_digits) == 8:
                    ncm_code = "%s.%s.%s" % (ncm_digits[:4], ncm_digits[4:6], ncm_digits[6:])
                _logger.info("NCM '%s' not found in DB. Creating it automatically.", ncm_code)
                ncm_id = env['account.ncm'].create({
                    'code': ncm_code,
                    'name': 'NCM Importado Automaticamente'
                })
            
        if ncm_id:
            product.write({'l10n_br_ncm_id': ncm_id.id})
            updated_count += 1
            _logger.info("Updated product ID %s - %s (%s) with NCM: %s", product.id, product.name, product.default_code, ncm_id.code)
        else:
            _logger.warning("NCM '%s' not found in DB for product %s (%s).", ncm, product.name, product.default_code)
            
    _logger.info("Finished. Successfully updated %d products.", updated_count)
