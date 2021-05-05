import datetime

from odoo import fields, models, exceptions, api
import re

from odoo.exceptions import ValidationError


class BiddingPackage(models.Model):
    _name = "mg.bidding.package"
    _description = "Package Record"
    _rec_name = "name"

    name = fields.Char(string="Name package")
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
    is_publish = fields.Boolean(char="Is public", default=False)
    is_auto = fields.Boolean(string="Auto", default=False)
    publish_time = fields.Datetime(datetime="Public time", readonly=True)
    publish_time_plan = fields.Datetime(datetime="Public time plan")
    duration_time = fields.Integer(integer="Duration time")
    is_real = fields.Boolean(string="Is real package", default=True)
    cargo_id = fields.Many2many("mg.cargo", 'id', string="Cargo")

    @api.onchange('return_date')
    def onchange_return_date(self):
        for bdp in self:
            if bdp.return_date is not False:
                if bdp.return_date <= bdp.receive_date or bdp.return_date <= datetime.datetime.now():
                    raise exceptions.ValidationError("Impossible")

    def _check_expiry(self):
        package_orders = self.env['mg.bidding.package'].search([])
        for order in package_orders:
            today = fields.Datetime.now()
            if order.publish_time_plan <= today:
                order.is_publish = True
                if order.publish_time is False:
                    order.publish_time = fields.Datetime.now()
            if order.publish_time is not False:
                duration = datetime.timedelta(minutes=order.duration_time) + order.publish_time
                if duration <= fields.Datetime.now():
                    order.is_publish = False
