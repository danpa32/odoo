# -*- coding: utf-8 -*-
from email.policy import default

from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.types'
    _description = "Real estate property type description"
    _order = "sequence, name asc"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string="Properties",
        help="Properties of this type"
    )
    sequence = fields.Integer(string="Sequence", default=1, help="Used to order property types in the UI")
    offer_ids = fields.One2many(string="Offers", comodel_name="estate.property.offer", inverse_name="property_type_id",
                                readonly=True, copy=False)
    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count",
        help="Count of offers for the property.",
    )

    # -------------------------------------------------------------------------
    # COMPUTED Methods
    # -------------------------------------------------------------------------
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # -------------------------------------------------------------------------
    # SQL Constraints
    # -------------------------------------------------------------------------
    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'Property type name must be unique.'),
    ]