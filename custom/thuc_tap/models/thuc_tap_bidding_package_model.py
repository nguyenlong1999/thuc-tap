import datetime

from custom.thuc_tap.constant.thuc_tap_status_tag import StatusTag
from custom.thuc_tap.constant.thuc_tap_type_tag import TypeTag
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
        ("-1", "Hủy"),
        ("0", "Chưa nhận"),
        ("1", "Đã duyệt"),
        ("2", "Chờ xác nhận"),
    ], string="status", required=True, default="0")
    from_depot = fields.Many2one("mg.depot", string="From Depot", required=True)
    to_depot = fields.Many2one("mg.depot", string="To Depot", required=True)
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

    bidding_order_id = fields.One2many('mg.bidding.order', 'package_id', string='Bidding Order', copy=False)

    cargo_id = fields.Many2many("mg.cargo", 'id', string="Cargo",
                                domain="[('from_depot', '=', from_depot),"
                                       "('to_depot', '=', to_depot)]")

    @api.model
    def create(self, values):
        values['code'] = self.env['ir.sequence'].next_by_code('mg.bidding.package')
        return super(BiddingPackage, self).create(values)

    @api.onchange('return_date')
    def onchange_return_date(self):
        for bdp in self:
            if bdp.return_date is not False:
                if bdp.return_date <= bdp.receive_date or bdp.return_date <= datetime.datetime.now():
                    raise exceptions.ValidationError("Impossible")

    @api.onchange("from_depot")
    def get_from_address(self):
        self.check_from_address()

    @api.onchange("to_depot")
    def get_to_address(self):
        self.check_to_address()

    def check_from_address(self):
        for bdp in self:
            if bdp.from_depot.id is not False:
                from_depot = self.env['mg.depot'].search([('id', '=', bdp.from_depot.id)])
                if bdp.from_depot.id == bdp.to_depot.id:
                    raise exceptions.ValidationError("Impossible depot")
                bdp.from_address = from_depot.street + ", " + from_depot.state_id.name + ", " + from_depot.country_id.name

    def check_to_address(self):
        for bdp in self:
            if bdp.to_depot.id is not False:
                to_depot = self.env['mg.depot'].search([('id', '=', bdp.to_depot.id)])
                if bdp.from_depot.id == bdp.to_depot.id:
                    raise exceptions.ValidationError("Impossible depot")
                bdp.to_address = to_depot.street + ", " + to_depot.state_id.name + ", " + to_depot.country_id.name

    @api.onchange("publish_time_plan")
    def onchange_publish_time_plan(self):
        for bdp in self:
            if bdp.publish_time_plan is not False:
                if bdp.publish_time_plan < datetime.datetime.now():
                    raise exceptions.ValidationError("Must be larger than the current time")

    def _check_expiry(self):
        package_orders = self.env['mg.bidding.package'].search([])
        for order in package_orders:
            today = fields.Datetime.now()
            if order.publish_time_plan is not False:
                if order.publish_time_plan <= today and order.status == StatusTag.STATUS_UNCONFIMRED:
                    order.is_publish = True
                    if order.publish_time is False:
                        order.publish_time = fields.Datetime.now()
            if order.publish_time is not False:
                duration = datetime.timedelta(minutes=order.duration_time) + order.publish_time
                if duration <= fields.Datetime.now():
                    order.is_publish = False

    def action_browse(self):
        for bdp in self:
            if bdp.is_publish is False:
                if bdp.publish_time is False:
                    bdp.is_publish = True
                    bdp.publish_time = fields.Datetime.now()
            else:
                raise exceptions.ValidationError("Đã duyệt")

    def action_browse_order(self):
        for bdp in self:
            if bdp.status == StatusTag.STATUS_WAIT:
                bdp.status = StatusTag.STATUS_APPROVED
                self.env['mg.bidding.order'].change_type(bdp.bidding_order_id.id, TypeTag.TYPE_APPROVED)
        return True

    def change_status(self, id, status):
        package_record = self.search([('id', '=', id)])
        package_record.write({'status': status})
        return True

    def unlink(self):
        for cargo in self.cargo_id:
            self.env['mg.cargo'].update_bidding_package(cargo.id, False)
        self.status = StatusTag.STATUS_CANCEL
        self.is_publish = False

    def delete_and_clone(self, id):
        self.change_status(id, StatusTag.STATUS_CANCEL)
        package_id = self.browse(id).copy({'status': StatusTag.STATUS_UNCONFIMRED}).id
        list_cargo = self.search([('id', '=', id)]).cargo_id

        print(list_cargo)
        print(package_id)
        for cargo in list_cargo:
            print(cargo.id)
            self.env['mg.cargo'].update_bidding_package(cargo.id, package_id)

    # def copy(self, default={}):
    #     default['status'] = StatusTag.STATUS_UNCONFIMRED
    #     rec = super(BiddingPackage, self).copy(default=default)
    #     return rec
