from odoo import api,fields,models,tools


class MxReceiptVoucher(models.Model):
    _inherit = 'mx.receipt.voucher'

    account_id = fields.Many2one(
        'account.account',
        string="Account",context={'formatted_display_name': False},
        domain="[('account_type', '=', 'asset_cash')]"
    )
    project_name = fields.Char(
        string='Project Name',
        compute='_compute_analytic_details')
    salesman = fields.Char(compute='_compute_analytic_details')
    project_location = fields.Char(
        string='Project Location',
        compute='_compute_analytic_details'
    )

    @api.depends('voucher_line_ids.analytic_distribution')
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
        receipt_account_ids = {}
        for receipt in self:
            account_ids = set()
            analytic_distribution = receipt.voucher_line_ids.analytic_distribution
            if analytic_distribution:
                for key in analytic_distribution.keys():
                    for acc_id in key.split(','):
                        acc_id = acc_id.strip()
                        if acc_id.isdigit():
                            account_ids.add(int(acc_id))
            receipt_account_ids[receipt.id] = account_ids
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
            order_ids = receipt_account_ids.get(order.id, set())
            for account in accounts:
                if account.id not in order_ids:
                    continue
                if account.plan_id.id == project_plan_id:
                    project_names.add(account.name)
                elif account.plan_id.id == salesman_plan_id:
                    salesman_names.add(account.name)
                elif account.plan_id.id == region_plan_id:
                    project_locations.add(account.name)
            receipt.project_name = ', '.join(sorted(project_names))
            receipt.salesman = ', '.join(sorted(salesman_names))
            receipt.project_location = ', '.join(sorted(project_locations))