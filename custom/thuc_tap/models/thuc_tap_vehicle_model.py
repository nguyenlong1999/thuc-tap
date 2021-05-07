from odoo import fields, models, exceptions, api
import re

from odoo.exceptions import ValidationError


class Vehicle(models.Model):
    _name = "mg.vehicle"
    _description = "Vehicle"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    tonnage = fields.Float(Float="Tonnage", required=True)
    type = fields.Char(string="Type", required=True)
    license_plate = fields.Char(string="License plate", required=True)
    color = fields.Char(string="Color", required=True)
    status = fields.Char(string="Status", required=True)
