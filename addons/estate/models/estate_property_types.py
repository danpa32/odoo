# -*- coding: utf-8 -*-
from email.policy import default

from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.types'
    _description = "Real estate property type description"

    name = fields.Char(string="Name", required=True)
