from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    name_arabic = fields.Char()
    street = fields.Char(translate=True)
    street2 = fields.Char(translate=True)
    city = fields.Char(translate=True)
    building_no = fields.Char(translate=True)
    district = fields.Char(translate=True)
    add_no = fields.Char(translate=True)


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    name = fields.Char(string='State Name', required=True, translate=True,
               help='Administrative divisions of a country. E.g. Fed. State, Department, Canton')


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    iban = fields.Char(string="IBAN")
