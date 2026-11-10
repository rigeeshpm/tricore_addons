from odoo import fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

    def get_invoice_region(self):
        self.ensure_one()
        region_plan = self.env['account.analytic.plan'].search(
            [('name', '=ilike', 'Region')],
            limit=1
        )
        if not region_plan:
            return ""

        # Collect all unique account IDs across all invoice lines
        account_ids = set()
        for line in self.invoice_line_ids:
            if not line.analytic_distribution:
                continue
            for key in line.analytic_distribution.keys():
                for acc_id in key.split(','):
                    if acc_id.isdigit():
                        account_ids.add(int(acc_id))

        if not account_ids:
            return ""

        # Find the first account matching the 'Region' plan
        region_account = self.env['account.analytic.account'].search([
            ('id', 'in', list(account_ids)),
            ('plan_id', '=', region_plan.id)
        ], limit=1)

        return region_account.name if region_account else ""
