# -*- coding: utf-8 -*-
from email.policy import default

from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real estate property offer description"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        default='accepted',
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True, ondelete='cascade')
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete='cascade')
