from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Cargo(models.Model):
    _name = "mg.cargo"
    _description = "Cargo"
    _code = "code"

    code = fields.Char(String='code')
    name = fields.Char(String='Name', required=True)

    length = fields.Float(String='Length', required=True)
    weight = fields.Float(String='Weight', required=True)
    height = fields.Float(String='Height', required=True)
    total_weight = fields.Float(String='Total weight', required=True)

    from_depot = fields.Many2one('mg.depot', 'From', required=True)
    to_depot = fields.Many2one('mg.depot', 'To', required=True)
    total_distance = fields.Float(String='Total distance', required=True)

    bidding_package_id = fields.Many2many('mg.bidding.package', 'id', String='Bidding package')

    size_standard_id = fields.One2many('mg.size.standard', 'id', String='Size standard')
