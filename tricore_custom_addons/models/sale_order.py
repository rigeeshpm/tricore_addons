from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_name = fields.Char(
        string='Project Name',
        compute='_compute_project_details',
        store=True
    )

    project_location = fields.Char(
        string='Project Location',
        compute='_compute_project_details',
        store=True
    )

    @api.depends('order_line.analytic_distribution')
    def _compute_project_details(self):
        project_plan = self.env['account.analytic.plan'].search(
            [('name', '=ilike', 'Project')],
            limit=1
        )
        for order in self:
            project_names = set()
            project_locations = set()

            if project_plan:
                # Collect all account IDs from all lines for this order
                account_ids = set()
                for line in order.order_line:
                    if not line.analytic_distribution:
                        continue
                    for key in line.analytic_distribution.keys():
                        for acc_id in key.split(','):
                            if acc_id.isdigit():
                                account_ids.add(int(acc_id))

                if account_ids:
                    # Fetch accounts that belong specifically to the 'Project' plan
                    accounts = self.env['account.analytic.account'].search([
                        ('id', 'in', list(account_ids)),
                        ('plan_id', '=', project_plan.id)
                    ])
                    for account in accounts:
                        project_names.add(account.name)
                        if account.partner_id and account.partner_id.contact_address:
                            project_locations.add(account.partner_id.contact_address)

            order.project_name = ', '.join(sorted(project_names))
            order.project_location = ', '.join(sorted(project_locations))



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    remarks = fields.Text()