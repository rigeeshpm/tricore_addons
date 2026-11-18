from odoo import _,api, fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    @api.depends('code')
    @api.depends_context(
        'company',
        'formatted_display_name',
        'from_bill',
        'no_account_hierarchy'
    )
    def _compute_display_name(self):
        super()._compute_display_name()
        if self.env.context.get('no_account_hierarchy'):
            for account in self:
                account.display_name = account.name or ''
