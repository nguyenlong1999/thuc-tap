from odoo import models, fields


class Depot(models.Model):
    _name = 'mg.depot'
    _inherit ='mg.address'
    _description = 'Information Depots'

    name = fields.Char(string='Name', required=True)
    latitude = fields.Float(string='latitude')
    longitude = fields.Float(string='longitude')
    status = fields.Selection({
        ('1', 'active'),
        ('-1', 'deactive')
    })