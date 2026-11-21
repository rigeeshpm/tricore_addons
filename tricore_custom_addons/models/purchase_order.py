from odoo import api, fields, models, tools


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    attn = fields.Char(string="Attn")
    validity = fields.Char(string="Validity")
    narration = fields.Text("Narration")
    partner_id = fields.Many2one(
        'res.partner', string='Vendor', required=True, change_default=True,
        tracking=True, check_company=True, index=True,
        help="You can find a vendor by its Name, TIN, Email or Internal Reference.",
        domain="[('supplier_rank','>',0)]"
    )


