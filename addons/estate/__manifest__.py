# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate',
    'version': '0.1',
    'summary': 'The Real Estate Advertisement module',
    'description': "",
    'website': 'http://localhost:8069',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/estate_property_tag_views.xml',
        'data/estate_property_types_views.xml',
        'data/estate_property_offer_views.xml',
        'data/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_views.xml',
        'views/res_users.xml',
    ],
    'demo': [
    ],
    'css': [
        'static/src/css/crm.css',
        'static/src/css/estate_form.css'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
