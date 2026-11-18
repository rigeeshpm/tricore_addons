from odoo import api,fields,models,tools


class payment_voucher(models.Model):
    _inherit = 'mx.payment.voucher'

    account_id = fields.Many2one(
        'account.account',
        string="Account",
        domain="[('account_type', '=', 'asset_cash')]"
    )

# class MxVoucherLines(models.Model):
#     _inherit = 'mx.payment.voucher.line'

    # account_id = fields.Many2one(
    #     'account.account',
    #     string="Account",
    #     domain="[('account_type', '=', 'asset_cash')]"
    # )
