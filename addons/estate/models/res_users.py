from odoo import api, models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    # -------------------------------------------------------------------------
    # Fields
    # -------------------------------------------------------------------------
    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='salesperson_id',
        string='Properties',
        domain=[('state', 'in', ['new', 'offer_received'])],
    )