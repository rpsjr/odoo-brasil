{  # pylint: disable=C8101,C8103
    'name': 'Odoo Next - Enable tax calculations',
    'description': 'Enable Tax Calculations',
    'version': '14.0.1.0.0',
    'category': 'Localization',
    'author': 'Trustcode',
    'license': 'OEEL-1',
    'website': 'http://www.odoo-next.com,br',
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
        'Felipe Paloschi <paloschi.eca@gmail.com>',
    ],
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/fiscal_position.xml',
        'views/account_tax.xml',
        'views/product.xml',
        'views/base_account.xml',
        'views/account_move_line.xml',
        'wizard/account_move_reversal_view.xml',
        'wizard/payment_move_line.xml',
    ],
    'post_init_hook': 'post_init',
}

