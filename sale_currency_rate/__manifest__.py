# -*- coding: utf-8 -*-
{
    'name': "Sale Currency Rate",

    'summary': """
        This module helps to show currency rate in the Sale Orders form view for multi-currency companies.        
    """,

    'description': """
        This module helps to show currency rate in the Sale Orders form view for multi-currency companies.
    """,

    'author': "Agung Sepruloh",
    'website': "https://github.com/agungsepruloh",
    'maintainers': ['agungsepruloh'],
    'license': 'OPL-1',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Sales',
    'version': '17.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],

    # only loaded in demonstration mode
    'demo': [],

    'images': ['static/description/banner.gif'],
    'application': True,
}

