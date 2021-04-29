# -*- coding: utf-8 -*-
# from odoo import http


# class ThucTap(http.Controller):
#     @http.route('/thuc_tap/thuc_tap/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/thuc_tap/thuc_tap/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('thuc_tap.listing', {
#             'root': '/thuc_tap/thuc_tap',
#             'objects': http.request.env['thuc_tap.thuc_tap'].search([]),
#         })

#     @http.route('/thuc_tap/thuc_tap/objects/<model("thuc_tap.thuc_tap"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('thuc_tap.object', {
#             'object': obj
#         })
