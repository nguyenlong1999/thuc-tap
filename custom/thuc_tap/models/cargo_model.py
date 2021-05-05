import ast

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
    total_distance = fields.Char(String='Total distance', readonly=True)

    bidding_package_id = fields.Many2many('mg.bidding.package', 'id', String='Bidding package', readonly=True)
    size_standard_id = fields.Many2one('mg.size.standard', 'id', String='Size standard')

    def call_api(self, from_depot, to_depot):
        url = 'https://maps.googleapis.com/maps/api/directions/json?mode=driving&transit_routing_preference=less_driving'
        fr = '&origin=' + str(from_depot.latitude) + ',' + str(from_depot.longitude) + ''
        to = '&destination=' + str(to_depot.latitude) + ',' + str(to_depot.longitude) + ''
        key = '&key=AIzaSyCmzEKuZOtAuDR5-iHmJvLScbSolUJEhBk'
        return self.get_dict(url + fr + to + key)

    def get_dict(self, str):
        result = requests.get(str).content
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
            if result['status'] == 'ZERO_RESULTS':
                raise ValidationError(_('Cannot calculate distance!!'))

            routes = self.list_to_dict(result['routes'])
            legs = routes['legs'][0][0]
            self.total_distance = legs['distance']['text']
