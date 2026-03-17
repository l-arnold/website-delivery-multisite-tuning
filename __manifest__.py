{
    'name': 'Website Delivery - Multi-Website Filter Fix',
    'version': '14.0.1.0.0',
    'category': 'Website',
    'summary': 'Fixes delivery method filtering to respect website_id in multi-website setups',
    'description': """
Website Delivery Multi-Website Filter
======================================

Fixes a bug in Odoo 14.0.0 where delivery methods are not filtered by website_id.

Without this module, all published delivery methods for a company are shown
on every website, regardless of their website_id assignment.

This module overrides sale.order._get_delivery_methods() to properly filter
by website_id.

Bug Context:
- Odoo 14.0.0 (2021-09-16) does not filter delivery methods by website
- This causes multi-website setups to show all methods on all sites
- Solved in later Odoo versions, but this backports the fix

Author: Landis Arnold / Nomadic Inc.
Date: March 2026
    """,
    'author': 'Nomadic Inc.',
    'website': 'https://nomadic.net',
    'depends': [
        'website_sale_delivery',
    ],
    'data': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
