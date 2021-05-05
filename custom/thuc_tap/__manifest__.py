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
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/bidding_package.xml',
        'views/size_standard.xml',
        'views/depot.xml',
        'views/cargo_view.xml',
        'data/sequence_bidding_package.xml',
        'data/sequence_size_standard.xml',
        'data/sequence_cargo.xml',
        'data/quotation_cron_package.xml'
    ],
    'installable': True,
    'application': True,
    'aotu_install': False,
}
