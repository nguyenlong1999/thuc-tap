from custom.thuc_tap.constant.thuc_tap_constant import Constant
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
    company_id = fields.Char(string='Company', required=True)
    status = fields.Char(string="Status", required=True)
    order = fields.Many2many('mg.bidding.order', string='Bidding Order')

    def capacity_used(self, vehicle):
        if not vehicle.order:
            return Constant.VOLUME_CONTAINED_EMPTY
        total_weigth = 0
        for order in vehicle.order:
            total_weigth += self.env['mg.bidding.order'].real_weigth(order.package_id)
        return total_weigth

    def free_volume(self, vehicle):
        print('capacity', self.capacity_used(vehicle))
        print('tonnage', vehicle.tonnage)
        return vehicle.tonnage - self.capacity_used(vehicle)
