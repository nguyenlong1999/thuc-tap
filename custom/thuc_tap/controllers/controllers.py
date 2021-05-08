from custom.thuc_tap.constant.thuc_tap_status_tag import StatusTag
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
