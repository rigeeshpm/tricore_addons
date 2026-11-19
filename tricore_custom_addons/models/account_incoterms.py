from odoo import api, fields, models, tools


class AccountIncoterms(models.Model):
    _inherit = 'account.incoterms'

    @api.depends('code')
    def _compute_display_name(self):
        for incoterm in self:
            incoterm.display_name = incoterm.code