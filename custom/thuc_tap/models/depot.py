from odoo import models, fields


class Depot(models.Model):
    _name = 'mg.depot'
    _description = 'Information Depots'

    name = fields.Char(string='Name', required=True)
    street = fields.Char(string='Street', required=True)
    zip = fields.Char(string='ZIP')
    city = fields.Char(string='City')
    country_id = fields.Many2one('res.country', string='Country')
    province_id = fields.Many2one('res.country.state', string='Province', domain="[('country_id','=',country_id)]")
    district = fields.Char(string='District')
    ward = fields.Char(string='Ward')
    latitude = fields.Float(string='latitude')
    longitude = fields.Float(string='longitude')
    status = fields.Selection({
        ('1', 'active'),
        ('-1', 'deactive')
    })
