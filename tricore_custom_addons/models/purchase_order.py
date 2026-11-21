from odoo import api, fields, models, tools


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    attn = fields.Char(string="Attn")
    validity = fields.Char(string="Validity")
    narration = fields.Text("Narration")


