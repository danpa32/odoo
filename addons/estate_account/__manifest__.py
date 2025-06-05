# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate Account',
    'version': '0.1',
    'summary': 'The Real Estate Account module',
    'description': "",
    'website': 'http://localhost:8069',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'css': [
        'static/src/css/crm.css',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
