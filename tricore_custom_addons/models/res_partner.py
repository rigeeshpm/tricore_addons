from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    name_ar = fields.Char(placeholder='Name in Arabic')
    street = fields.Char(translate=True)
    street2 = fields.Char(translate=True)
    city = fields.Char(translate=True)
    building_no = fields.Char(translate=True)
    add_no = fields.Char(translate=True)

    def translate_to_arabic_digits(self, text):
        if not text:
            return ""
        trans_table = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
        return str(text).translate(trans_table)


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    name = fields.Char(string='State Name', required=True, translate=True,
               help='Administrative divisions of a country. E.g. Fed. State, Department, Canton')

class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    iban = fields.Char(string="IBAN")
