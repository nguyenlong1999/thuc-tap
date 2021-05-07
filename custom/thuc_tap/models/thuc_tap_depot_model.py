from odoo import models, fields, api


class Depot(models.Model):
    _name = 'mg.depot'
    _description = 'Information Depots'

    name = fields.Char(string='Name', required=True)
    street = fields.Char(string='Street', required=True)
    zip = fields.Char(string='ZIP')
    city = fields.Char(string='City')
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string='Province', domain="[('country_id','=',country_id)]")
    district = fields.Char(string='District')
    ward = fields.Char(string='Ward')
    latitude = fields.Float(string='latitude')
    longitude = fields.Float(string='longitude')
    status = fields.Selection({
        ('1', 'active'),
        ('-1', 'deactive')
    })

    @api.model
    def _geo_localize(self, street='', zip='', city='', state='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(street=street, zip=zip, city=city, state=state, country=country)
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            search = geo_obj.geo_query_address(city=city, state=state, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    def geo_localize(self):
        for depot in self.with_context(lang='en_US'):
            result = self._geo_localize(depot.street,
                                        depot.zip,
                                        depot.city,
                                        depot.state_id.name,
                                        depot.country_id.name)

            if result:
                depot.write({
                    'latitude': result[0],
                    'longitude': result[1],
                })
        return True
