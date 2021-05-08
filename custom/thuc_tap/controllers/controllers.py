
from custom.thuc_tap.constant.thuc_tap_status_tag import StatusTag
# -*- coding: utf-8 -*-
import datetime
import time
from custom.thuc_tap.models.thuc_tap_bidding_package_model import BiddingPackage

from odoo import http
from odoo.http import request


class ThucTap(http.Controller):

    # @http.route('/api/accept_bidding', type='json', auth='user')
    # def add_vehicle(self, **rec):
    #     if request.jsonrequest:
    #         # id vehicle


    @http.route('/api/accept_bidding', type='json', auth='user')
    def get_package(self, **rec):
        if request.jsonrequest:
            # id bidding package
            bidding_package_model = request.env['mg.bidding.package']
            package = bidding_package_model.browse(rec['id'])
            if not package:
                return {'status': StatusTag.INVALID_ID, 'response': 'id is invalid', 'message': 'Failed'}
            if not package.is_publish:
                return {'status': StatusTag.PACKAGE_NOT_PUBLISH, 'response': 'Package is not publish!',
                        'message': 'Failed'}
            bidding_package_model.change_status(rec['id'], StatusTag.STATUS_WAIT)
            vals = {
                'name': 'order' + package.name,
                'package_id': package.id,
                'from_depot': package.from_depot.id,
                'to_depot': package.to_depot.id,
                'receive_date': package.receive_date,
                'return_date': package.return_date,
                'from_address': package.from_address,
                'to_address': package.to_address,
            }
            bidding_order_model = request.env['mg.bidding.order']
            create_order = bidding_order_model.create(vals)
            if not create_order:
                return {'status': StatusTag.SERVER_ERROR, 'response': 'Server Error', 'message': 'Failed'}
            vals = {
                'id': create_order.id,
                'code': create_order.code,
                'name': create_order.name,
            }
        return {'status': StatusTag.SUCCESS, 'response': vals, 'message': 'Success'}

    def datetime_to_utctime(self):
        dt = datetime.datetime.strptime(self, "%Y-%m-%d %H:%M:%S")
        utc_struct_time = time.gmtime(time.mktime(dt.timetuple()))
        utc_dt = datetime.datetime.fromtimestamp(time.mktime(utc_struct_time))
        return str(utc_dt)

    @http.route('/get_bidding_package', type='http', auth='none', methods=['GET'], csrf=False)
    def get_all_bidding(self):
        list_bidding = request.env['mg.bidding.package'].sudo().search([])
        bidding = []
        for rec in list_bidding:
            vals = {
                'id': rec.id,
                'name': rec.name,
                'status': rec.status,
                'from_depot': rec.from_depot.id,
                'to_depot': rec.to_depot.id,
                'cargo_id': rec.cargo_id.id,
            }
            bidding.append(vals)
        data = {
            'status': '200',
            'message': 'success',
            'response': bidding,
        }
        return data

    @http.route('/create_bidding_package', type='json', auth='user', methods=['POST'])
    def create_bidding_package(self, **rec):
        global args
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'name': rec['name'],
                    'status': rec['status'],
                    'from_depot': rec['from_depot'],
                    'to_depot': rec['to_depot'],
                    'receive_date': rec['receive_date'],
                    'return_date': rec['return_date'],
                    'from_address': rec['from_address'],
                    'to_address': rec['to_address'],
                    'duration_time': rec['duration_time'],
                    'publish_time_plan': rec['publish_time_plan'],
                    'is_auto': rec['is_auto'],
                    'is_real': rec['is_real'],
                    'cargo_id': rec['cargo_id']
                }
                if rec['from_depot'] is not False:
                    from_depot = request.env['mg.depot'].sudo().search([('id', '=', int(rec['from_depot']))])
                    vals['from_address'] = from_depot.street + ", " + from_depot.state_id.name + ", " + from_depot.country_id.name
                if rec['to_depot'] is not False:
                    to_depot = request.env['mg.depot'].sudo().search([('id', '=', int(rec['to_depot']))])
                    vals['to_address'] = to_depot.street + ", " + to_depot.state_id.name + ", " + to_depot.country_id.name
                if rec['publish_time_plan'] is not False:
                    vals['publish_time_plan'] = ThucTap.datetime_to_utctime(rec['publish_time_plan'])
                if rec['receive_date'] is not False:
                    vals['receive_date'] = ThucTap.datetime_to_utctime(rec['receive_date'])
                if rec['return_date'] is not False:
                    vals['return_date'] = ThucTap.datetime_to_utctime(rec['return_date'])
                new_bidding_package = request.env['mg.bidding.package'].sudo().create(vals)

                args = {
                    'status': '200',
                    'message': 'Success',
                    'data': {
                        'id': new_bidding_package.id,
                        'name': new_bidding_package.name,
                        'code': new_bidding_package.code
                    },
                }
            else:
                args = {
                    'status': '404',
                    'message': 'Create false ',

                }
        else:
            args = {
                'status': '404',
                'message': 'False',

            }
        return args

    @http.route('/update_bidding_package/<int:bidding_package_id>', type='json', auth='user', methods=['POST'])
    def update_bidding_package(self, bidding_package_id, **rec):
        global args
        old_package = request.env['mg.bidding.package'].sudo().search([('id', '=', bidding_package_id)])
        if len(old_package) > 0:
            if request.jsonrequest:
                if rec['name']:
                    vals = {
                        'name': rec['name'],
                        'status': rec['status'],
                        'from_depot': rec['from_depot'],
                        'to_depot': rec['to_depot'],
                        'receive_date': rec['receive_date'],
                        'return_date': rec['return_date'],
                        'from_address': rec['from_address'],
                        'to_address': rec['to_address'],
                        'duration_time': rec['duration_time'],
                        'publish_time_plan': rec['publish_time_plan'],
                        'is_auto': rec['is_auto'],
                        'is_real': rec['is_real'],
                        'cargo_id': rec['cargo_id']
                    }
                    if rec['from_depot'] is not False:
                        from_depot = request.env['mg.depot'].sudo().search([('id', '=', int(rec['from_depot']))])
                        vals[
                            'from_address'] = from_depot.street + ", " + from_depot.state_id.name + ", " + from_depot.country_id.name
                    if rec['to_depot'] is not False:
                        to_depot = request.env['mg.depot'].sudo().search([('id', '=', int(rec['to_depot']))])
                        vals[
                            'to_address'] = to_depot.street + ", " + to_depot.state_id.name + ", " + to_depot.country_id.name
                    if rec['publish_time_plan'] is not False:
                        vals['publish_time_plan'] = ThucTap.datetime_to_utctime(rec['publish_time_plan'])
                    if rec['receive_date'] is not False:
                        vals['receive_date'] = ThucTap.datetime_to_utctime(rec['receive_date'])
                    if rec['return_date'] is not False:
                        vals['return_date'] = ThucTap.datetime_to_utctime(rec['return_date'])
                    old_package.write(vals)
                    args = {
                        'status': '200',
                        'message': 'Success',
                        'data': {
                            'id': old_package.id,
                            'name': old_package.name,
                            'code': old_package.code
                        },
                    }
                else:
                    args = {
                        'status': '404',
                        'message': 'False update package',
                    }
        else:
            args = {
                'status': '404',
                'message': 'Not found package',
            }
        return args

    @http.route('/delete_bidding_package/<int:bidding_package_id>', type='json', auth='user', methods=['POST'])
    def delete_bidding_package(self, bidding_package_id, **rec):
        global args
        old_package = request.env['mg.bidding.package'].sudo().search([('id', '=', bidding_package_id)])
        if len(old_package) > 0:
            old_package.unlink()
        else:
            args = {
                'status': '404',
                'message': 'Not found package',
        }
        return args
