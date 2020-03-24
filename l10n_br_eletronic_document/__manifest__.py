{  # pylint: disable=C8101,C8103
    'name': 'Odoo Next - Eletronic documents',
    'description': 'Enable Eletronic Documents',
    'version': '13.0.1.0.0',
    'category': 'Localization',
    'author': 'Trustcode',
    'license': 'OEEL-1',
    'website': 'http://www.odoo-next.com,br',
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
    ],
    'depends': [
        'account',
        'l10n_br_base',
        'l10n_br_base_address',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company.xml',
        'views/account_move.xml',
        'views/eletronic_document.xml',
        'views/eletronic_document_line.xml',
        'views/fiscal_position.xml',
        'reports/danfse_sao_paulo.xml',
        'reports/danfse_florianopolis.xml',
    ],
}
