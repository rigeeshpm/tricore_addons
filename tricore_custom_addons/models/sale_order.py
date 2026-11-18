from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    remark = fields.Text()
    project_name = fields.Char(
        string='Project Name',
        compute='_compute_project_details')
    salesman = fields.Char(compute='_compute_salesman')

    project_location = fields.Char(
        string='Project Location',
        compute='_compute_project_details',
        store=True
    )
    validity = fields.Char("Validity")
    attn = fields.Char("Attn")

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

    def _compute_salesman(self):
        sales_plan = self.env['account.analytic.plan'].search(
            [('name', '=ilike', 'Salesman')],
            limit=1
        )
        for order in self:
            salesman_names = set()
            if sales_plan:
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
                        ('plan_id', '=', sales_plan.id)
                    ])
                    for account in accounts:
                        salesman_names.add(account.name)

            order.salesman = ', '.join(sorted(salesman_names))



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    remarks = fields.Text()
    label_new = fields.Char(
        string='New Label',
    )

    def _compute_label_without_default_code(self):
        for line in self:
            label = line.label or ''
            default_code = line.product_id.default_code
            if default_code:
                prefix = f'[{default_code}]'
                if label.startswith(prefix):
                    label = label[len(prefix):]
            line.label_new = label
            return label
