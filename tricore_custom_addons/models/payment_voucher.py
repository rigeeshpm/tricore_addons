from odoo import api,fields,models,tools


class MxPaymentVoucher(models.Model):
    _inherit = 'mx.payment.voucher'

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
        # Fetch analytic plans
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

        # Collect analytic account IDs from all voucher lines
        all_account_ids = set()
        payment_account_ids = {}

        for payment in self:
            account_ids = set()

            for line in payment.voucher_line_ids:
                distribution = line.analytic_distribution or {}

                for key in distribution.keys():
                    for acc_id in key.split(','):
                        acc_id = acc_id.strip()

                        if acc_id.isdigit():
                            account_ids.add(int(acc_id))

            payment_account_ids[payment.id] = account_ids
            all_account_ids.update(account_ids)

        # Fetch all relevant analytic accounts in one query
        plan_ids = [
            plan_id for plan_id in [
                project_plan_id,
                salesman_plan_id,
                region_plan_id
            ] if plan_id
        ]

        accounts = self.env['account.analytic.account'].search([
            ('id', 'in', list(all_account_ids)),
            ('plan_id', 'in', plan_ids)
        ]) if all_account_ids and plan_ids else self.env['account.analytic.account']

        accounts_dict = {
            account.id: account
            for account in accounts
        }

        # Compute fields for each voucher
        for payment in self:

            project_names = set()
            salesman_names = set()
            project_locations = set()

            account_ids = payment_account_ids.get(payment.id, set())

            for account_id in account_ids:

                account = accounts_dict.get(account_id)

                if not account:
                    continue

                if account.plan_id.id == project_plan_id:
                    project_names.add(account.name)

                elif account.plan_id.id == salesman_plan_id:
                    salesman_names.add(account.name)

                elif account.plan_id.id == region_plan_id:
                    project_locations.add(account.name)

            payment.project_name = ', '.join(sorted(project_names))
            payment.salesman = ', '.join(sorted(salesman_names))
            payment.project_location = ', '.join(sorted(project_locations))

class MxVoucherLines(models.Model):
    _inherit = 'mx.payment.voucher.line'

    account_id = fields.Many2one(
        'account.account',
        string="Account",
        context={'formatted_display_name': False},
    )
