# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Thực tập',
    'version': '1.1',
    'summary': 'QUAN LY LOP HOC',
    'sequence': 1,
    'description': """QUAN LY LOP HOC""",
    'category': 'Productivity',
    'website': 'https://www.odoo.com/page/billing',
    'depends': [
        'mail',
        'web_google_maps'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/thuc_tap_bidding_package_view.xml',
        'views/thuc_tap_bidding_order_view.xml',
        'views/thuc_tap_size_standard_view.xml',
        'views/thuc_tap_depot_view.xml',
        'views/thuc_tap_cargo_view.xml',
        'views/thuc_tap_vehicle_view.xml',
        'data/sequence_bidding_package.xml',
        'data/sequence_size_standard.xml',
        'data/sequence_cargo.xml',
        'data/quotation_cron_package.xml',
        'data/quotation_cron_duration_order.xml',
    ],
    'installable': True,
    'application': True,
    'aotu_install': False,
}
