# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, models, fields
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real estate property description"

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    name = fields.Char(string="Name", required=True)
    description = fields.Text()
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", default=lambda self: fields.date.today() + relativedelta(months=3) ,copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], required=True, string="Status", copy=False, default='new')
    property_type_id = fields.Many2one("estate.property.types", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # -------------------------------------------------------------------------
    # SQL Constraints
    # -------------------------------------------------------------------------
    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
    ]

    # -------------------------------------------------------------------------
    # Python Constraints
    # -------------------------------------------------------------------------
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            """Selling price should be higher than 90% of expected price."""
            if record.selling_price < 0.9 * record.expected_price:
                raise UserError(
                    "The selling price must be at least 90% of the expected price."
                )

    # -------------------------------------------------------------------------
    # COMPUTED Fields
    # -------------------------------------------------------------------------
    total_area = fields.Float(
        string="Total Area (sqm)",
        compute="_compute_total",
        help="Total area of the property, computed as living area plus garden area."
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        help="Best offer received for the property."
    )

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------
    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    # -------------------------------------------------------------------------
    # ON-CHANGE
    # -------------------------------------------------------------------------
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # -------------------------------------------------------------------------
    # User Interface Actions
    # -------------------------------------------------------------------------
    def action_sell(self):
        """Mark the property as sold and set the selling price."""
        if self.state == 'canceled':
            raise UserError('You cannot sell a canceled property.')
        else:
            self.state = 'sold'

    def action_cancel(self):
        """Cancel the property listing."""
        if self.state == 'sold':
            raise UserError('You cannot cancel a sold property.')
        else:
            self.state = 'canceled'