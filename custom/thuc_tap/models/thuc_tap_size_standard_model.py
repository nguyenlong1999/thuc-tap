from odoo import fields, models, exceptions, api
import re

from odoo.exceptions import ValidationError


class SizeStandard(models.Model):
    _name = "mg.size.standard"
    _description = "Package Record"
    _code = "code"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    from_weight = fields.Float(Float="From weight", required=True)
    to_weight = fields.Float(Float="To weight", required=True)
    width = fields.Float(Float="Width", required=True)
    height = fields.Float(Float="Height", required=True)
    length = fields.Float(Float="Length", required=True)
    cargo_id = fields.One2many("mg.cargo", 'id', String="Cargo")
