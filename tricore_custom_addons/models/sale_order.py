from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    remark = fields.Text()
    project_name = fields.Char(
        string='Project Name',
        compute='_compute_analytic_details')
    salesman = fields.Char(compute='_compute_analytic_details')
    project_location = fields.Char(
        string='Project Location',
        compute='_compute_analytic_details'
    )
    validity = fields.Char("Validity")
    attn = fields.Char("Attn")
    eta = fields.Char("Expected Time of Arrival")

    @api.depends('analytic_distribution')
    def _compute_analytic_details(self):
        # Fetch the three analytic plans
        plans = self.env['account.analytic.plan'].search([
            '|', '|',
            ('name', '=ilike', 'Project'),
            ('name', '=ilike', 'Salesman'),
            ('name', '=ilike', 'Region'),
        ])
        plans_dict = {
            plan.name.lower(): plan.id
            for plan in plans
        }
        project_plan_id = plans_dict.get('project')
        salesman_plan_id = plans_dict.get('salesman')
        region_plan_id = plans_dict.get('region')
        # Collect all analytic account IDs from all orders
        all_account_ids = set()
        order_account_ids = {}
        for order in self:
            if (not order.analytic_distribution) and order.order_line.mapped('analytic_distribution'):
                order._compute_analytic_distribution()
            account_ids = set()
            if order.analytic_distribution:
                for key in order.analytic_distribution.keys():
                    for acc_id in key.split(','):
                        acc_id = acc_id.strip()
                        if acc_id.isdigit():
                            account_ids.add(int(acc_id))
            order_account_ids[order.id] = account_ids
            all_account_ids.update(account_ids)
        # Fetch all relevant analytic accounts in one query
        accounts = self.env['account.analytic.account'].search([
            ('id', 'in', list(all_account_ids)),
            ('plan_id', 'in', [
                plan_id for plan_id in [
                    project_plan_id,
                    salesman_plan_id,
                    region_plan_id
                ] if plan_id
            ])
        ]) if all_account_ids else self.env['account.analytic.account']
        # Compute the three fields
        for order in self:
            project_names = set()
            salesman_names = set()
            project_locations = set()
            order_ids = order_account_ids.get(order.id, set())
            for account in accounts:
                if account.id not in order_ids:
                    continue
                if account.plan_id.id == project_plan_id:
                    project_names.add(account.name)
                elif account.plan_id.id == salesman_plan_id:
                    salesman_names.add(account.name)
                elif account.plan_id.id == region_plan_id:
                    project_locations.add(account.name)
            order.project_name = ', '.join(sorted(project_names))
            order.salesman = ', '.join(sorted(salesman_names))
            order.project_location = ', '.join(sorted(project_locations))



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
