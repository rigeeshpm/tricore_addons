from odoo import fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

    def get_invoice_region(self):
        self.ensure_one()
        for line in self.invoice_line_ids:
            if not line.analytic_distribution:
                continue
            # Extract analytic account IDs from the line's distribution dictionary
            account_ids = [int(acc_id) for acc_id in line.analytic_distribution.keys()]
            if not account_ids:
                continue
            # Search for an account belonging to the 'Region' plan
            region_account = self.env['account.analytic.account'].search([
                ('id', 'in', account_ids),
                ('plan_id.name', 'ilike', 'region')
            ], limit=1)
            if region_account:
                return region_account.name
        return ""
