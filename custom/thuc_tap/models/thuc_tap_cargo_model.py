import ast

from custom.thuc_tap.constant.thuc_tap_constant import Constant
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import requests


class Cargo(models.Model):
    _name = "mg.cargo"
    _description = "Cargo"
    _code = "code"

    code = fields.Char(String='code', readonly=True)
    name = fields.Char(String='Name', required=True)

    length = fields.Float(String='Length', required=True)
    weight = fields.Float(String='Weight', required=True)
    height = fields.Float(String='Height', required=True)
    total_weight = fields.Float(String='Total weight', required=True)

    from_depot = fields.Many2one('mg.depot', 'From', required=True)
    to_depot = fields.Many2one('mg.depot', 'To', required=True)
    total_distance = fields.Char(String='Total distance')

    bidding_package_id = fields.Many2many('mg.bidding.package', 'id', String='Bidding package', readonly=True)
    size_standard_id = fields.Many2one('mg.size.standard', String='Size standard')

    @api.model
    def create(self, values):
        values['code'] = self.env['ir.sequence'].next_by_code('mg.cargo')
        return super(Cargo, self).create(values)

    def call_api(self, from_depot, to_depot):
        url = Constant.API_MAP_ROUTE_URL
        fr = '&origin=' + str(from_depot.latitude) + ',' + str(from_depot.longitude) + ''
        to = '&destination=' + str(to_depot.latitude) + ',' + str(to_depot.longitude) + ''
        key = '&key=' + Constant.API_MAP_ROUTE_KEY
        return self.get_dict(url + fr + to + key)

    def get_dict(self, string):
        result = requests.get(string).content
        result = ast.literal_eval(result.decode('utf-8'))
        return result

    def list_to_dict(self, lst):
        new_dict = {}
        for k, v in [(key, d[key]) for d in lst for key in d]:
            if k not in new_dict:
                new_dict[k] = [v]
            else:
                new_dict[k].append(v)
        return new_dict

    @api.onchange('to_depot')
    def onchange_to_depot(self):
        for rec in self:
            if not rec.to_depot:
                break
            if rec.to_depot == rec.from_depot:
                raise ValidationError(_('To depot invalid!!'))
            if not rec.from_depot:
                break

            result = self.call_api(rec.from_depot, rec.to_depot)
            if result['status'] == Constant.API_MAP_ZERO_RESULTS:
                raise ValidationError(_('Cannot calculate distance!!'))

            routes = self.list_to_dict(result['routes'])
            legs = routes['legs'][0][0]
            rec.write({
                'total_distance': legs['distance']['text']
            })

    @api.onchange('total_weight')
    def onchange_total_weight(self):
        if self.total_weight < self.weight:
            raise ValidationError(_('Total weight invalid'))

    @api.onchange('size_standard_id')
    def onchange_size_standard_id(self):
        size_infor = self.env['mg.size.standard'].search([('id', '=', self.size_standard_id.id)])
        self.height = size_infor.height
        self.weight = size_infor.weight

    @api.onchange('weight')
    def onchange_weight(self):
        size_infor = self.env['mg.size.standard'].search([('id', '=', self.size_standard_id.id)])
        if size_infor.weight < self.weight:
            raise ValidationError(_('Weight invalid'))

    @api.onchange('height')
    def onchange_height(self):
        size_infor = self.env['mg.size.standard'].search([('id', '=', self.size_standard_id.id)])
        if size_infor.height < self.height:
            raise ValidationError(_('Height invalid'))

    @api.onchange('length')
    def onchange_length(self):
        size_infor = self.env['mg.size.standard'].search([('id', '=', self.size_standard_id.id)])
        if size_infor.length < self.length:
            raise ValidationError(_('Length invalid'))

    def update_bidding_package(self, cargo_id, package_id):
        cargo_rec = self.search([('id', '=', cargo_id)])
        package = self.env['mg.bidding.package'].browse(package_id)
        cargo_rec.write({
            'bidding_package_id': package
        })
