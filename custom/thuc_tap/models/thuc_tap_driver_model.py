from odoo import fields, models, exceptions, api
import re

from odoo.exceptions import ValidationError


class Driver(models.Model):
    _name = "mg.driver"
    _description = "Driver"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    age = fields.Integer(Integer="Age", required=True)
    hometown = fields.Char(string="Hometown", required=True)
    id_card = fields.Integer(Integer="ID card", required=True)
    company_id = fields.Char(string="Company", required=True)
    status = fields.Char(string="status", required=True)
