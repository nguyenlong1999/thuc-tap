from odoo import fields, models, exceptions, api
import re

from odoo.exceptions import ValidationError


class BiddingPackage(models.Model):
    _name = "mg.bidding.package"
    _description = "Package Record"
    _rec_name = "name"

    name = fields.Char(string="Name package", required=True)
    code = fields.Char(string='Code')
    status = fields.Selection([
        ("0", "chưa nhận"),
        ("1", "đã duyệt"),
        ("2", "chờ xác nhận"),
    ], string="status", required=True, default="0")
    from_depot = fields.Char(string="From Depot", required=True)
    to_depot = fields.Char(string="To Depot", required=True)
    receive_date = fields.Datetime(string="Receive date", required=True)
    return_date = fields.Datetime(string="Return date", required=True)
    from_address = fields.Char(string="From Address", required=True)
    to_address = fields.Char(string="To Address", required=True)
    is_publish = fields.Boolean(char="Is public", required=True, default=True)
    is_auto = fields.Char(string="Auto", required=True)
    publish_time = fields.Integer(string="Public time", readonly=True)
    publish_time_plan = fields.Char(string="Public time plan", required=True)
    duration_time = fields.Integer(string="Duration time", required=True)
    is_real = fields.Boolean(string="Is real package", default=True)
    cargo_id = fields.Many2many("mg.cargo", 'id',String="Cargo")

    @api.onchange('return_date')
    def onchange_return_date(self):
        for bdp in self:
            if bdp.return_date is not False:
                if bdp.return_date <= bdp.receive_date:
                    raise exceptions.ValidationError("Impossible")


