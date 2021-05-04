from odoo import models, fields


class Address(models.TransientModel):
    _name = 'mg.address'
    _description = 'Address customer'

    street = fields.Char(string='Street', required=True)
    zip = fields.Char(string='ZIP')
    city = fields.Char(string='City')
    country_id = fields.Many2one('res.country',string='Country')
    province_id = fields.Many2one('res.country.state',string='Province', domain=[('country_id', '=', country_id.id)])
    district = fields.Char(string='District')
    ward = fields.Char(string='Ward')

