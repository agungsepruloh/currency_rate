# -*- coding: utf-8 -*-
{
    'name': "Invoice/Bills Currency Rate",

    'summary': """
        This module helps to show currency rate in the Invoices and Bills form view for multi-currency companies.
    """,

    'description': """
        This module helps to show currency rate in the Invoices and Bills form view for multi-currency companies.
    """,

    'author': "Agung Sepruloh",
    'website': "https://github.com/agungsepruloh",
    'maintainers': ['agungsepruloh'],
    'license': 'OPL-1',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': '18.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
    ],

    # only loaded in demonstration mode
    'demo': [],

    'images': ['static/description/banner.gif'],
    'application': True,
}

