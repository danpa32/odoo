# -*- coding: utf-8 -*-
from datetime import timedelta
from email.policy import default

from odoo import models, fields, api


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
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
        help="Number of days the offer is valid, default is 7 days.",
    )

    # -------------------------------------------------------------------------
    # SQL Constraints
    # -------------------------------------------------------------------------
    _sql_constraints = [
        ('check_price_positive', 'CHECK(price >= 0)', 'The expected price must be strictly positive.'),
    ]

    # -------------------------------------------------------------------------
    # COMPUTED Fields
    # -------------------------------------------------------------------------
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
        help="Deadline for the offer, computed as the sum of the create_date and the validity days of the offer.",
    )

    # -------------------------------------------------------------------------
    # COMPUTED Methods
    # -------------------------------------------------------------------------
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = (record.create_date or fields.Datetime.today()).date()
            deadline = record.date_deadline or fields.Date.today()
            record.validity = (deadline - create_date).days

    # -------------------------------------------------------------------------
    # User Interface Actions Methods
    # -------------------------------------------------------------------------
    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
            record.property_id.state = 'offer_received'