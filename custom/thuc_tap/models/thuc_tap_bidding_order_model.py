import datetime

from custom.thuc_tap.constant.thuc_tap_constant import Constant
from custom.thuc_tap.constant.thuc_tap_status_tag import StatusTag
from custom.thuc_tap.constant.thuc_tap_type_tag import TypeTag
from odoo import fields, models, exceptions, api
import re
from odoo.exceptions import ValidationError


class BiddingOrder(models.Model):
    _name = "mg.bidding.order"
    _description = "Order"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', readonly=True)
    package_id = fields.Many2one('mg.bidding.package', string='Package')
    type = fields.Selection([
        ("-1", "Hủy"),
        ("0", "Chưa điền thông tin"),
        ("1", "Đã duyệt"),
        ("2", "Đã điền thông tin xe"),
        ("3", "Reconfirm"),
    ], string="Type", required=True, default="0")
    status = fields.Selection([
        ("0", "Chưa xác nhận"),
        ("1", "Đã duyệt"),
        ("2", "Đã trả"),
    ], string="status", required=True, default="0")
    from_depot = fields.Many2one('mg.depot', 'From', required=True)
    to_depot = fields.Many2one('mg.depot', 'To', required=True)
    receive_date = fields.Datetime(string="Receive date", required=True)
    return_date = fields.Datetime(string="Return date", required=True)
    from_address = fields.Char(string='From address', required=True)
    to_address = fields.Char(string='To address', required=True)
    company_id = fields.Char(string='Company')
    vehicle = fields.Many2one('mg.vehicle', string='Driver')
    time_create = fields.Datetime(string='Time create')

    @api.onchange('package_id')
    def onchange_package_id(self):
        package = self.env['mg.bidding.package'].search([('id', '=', self.package_id.id)])
        if not package:
            return
        self.from_depot = package.from_depot
        self.to_depot = package.to_depot
        self.receive_date = package.receive_date
        self.return_date = package.return_date
        self.from_address = package.from_address
        self.to_address = package.to_address

    @api.model
    def create(self, vals_list):
        vals_list['time_create'] = fields.Datetime.now()
        rec = super(BiddingOrder, self).create(vals_list)
        return rec

    def change_type(self, id, type):
        order_record = self.search([('id', '=', id)])
        order_record.write({'type': type})
        return True

    def change_status(self, id, status):
        package_record = self.search([('id', '=', id)])
        package_record.write({'status': status})
        return True

    def _check_duration(self):
        order_recs = self.search([])
        for order in order_recs:
            if order.time_create is not False:
                duration = datetime.timedelta(minutes=Constant.BIDDING_ORDER_DURATION_MINUTES) + order.time_create
                if duration <= fields.Datetime.now() and not order.vehicle:
                    order.type = TypeTag.TYPE_CANCEL
                    bidding_package = self.env['mg.bidding.package']
                    bidding_package.change_status(order.package_id.id, StatusTag.STATUS_CANCEL)
                    return bidding_package.copy([('id', '=', order.package_id.id)])
        return True
