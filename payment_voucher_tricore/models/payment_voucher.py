from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError, ValidationError


class MxPaymentVoucher(models.Model):
	_name = 'mx.payment.voucher'
	_description = 'Payment Voucher'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	@api.depends('journal_id')
	def _compute_company_id(self):
		self.company_id = self.env.company.id
		self.currency_id = self.company_id.currency_id.id

	name = fields.Char(string="Reference", required=True, copy=False, readonly=True, index=True, tracking=True, default=lambda self: _("New"))
	account_id = fields.Many2one('account.account')
	voucher_date = fields.Date(default=fields.Datetime.now)
	journal_id = fields.Many2one('account.journal')
	voucher_line_ids = fields.One2many('mx.payment.voucher.line', 'voucher_id')
	state = fields.Selection([('draft', 'Draft'), ('post','Posted'), ('cancel','Cancelled')], "State", default='draft')
	company_id = fields.Many2one(comodel_name='res.company', string='Company',	store=True, readonly=True, compute='_compute_company_id')
	currency_id = fields.Many2one('res.currency', store=True, readonly=True, tracking=True, states={'draft': [('readonly', False)]},string='Currency')
	untaxed_amount = fields.Monetary(compute='_get_voucher_amount_details')
	tax = fields.Monetary(compute='_get_voucher_amount_details')
	total = fields.Monetary(compute='_get_voucher_amount_details')
	journal_entry_id = fields.Many2one('account.move')
	narration = fields.Char('Narration')


	def action_draft(self):
		if not self.journal_entry_id:
			raise UserError(_('The Journal entry doesn\'t exists.'))
		self.journal_entry_id.with_context(force_delete=True).unlink()
		self.state = 'draft'

	def unlink(self):
		for pv in self:
			if pv.name != 'New':
				raise UserError(_("This payment voucher can't delete."))
		return super(MxPaymentVoucher, self).unlink()

	@api.depends('voucher_line_ids.tax', 'voucher_line_ids.amount')
	def _get_voucher_amount_details(self):
		"""Calulating taxed and untaxed total of voucher"""
		for record in self:
			tax =0.0
			untaxed_amount = 0.0
			total = 0.0
			for line in record.voucher_line_ids:
				tax += line.tax_amount
				untaxed_amount += line.amount
			record.untaxed_amount = untaxed_amount
			record.tax = tax
			record.total = tax+untaxed_amount

	def post_journal(self):
		"""Creating journal entry for the voucher"""
		# `user_has_group` won't be bypassed by `sudo()` since it doesn't change the user anymore.
		if not self.env.su and not self.env.user.has_group('account.group_account_invoice'):
			raise AccessError(_("You don't have the access rights to post an invoice."))

		for voucher in self:
			if voucher.state == 'post':
				raise UserError(_(
					'The entry %s (id %s) is already posted.'
				) % (voucher.name, voucher.id))
		move_lines = []
		for line in self.voucher_line_ids:
			a = {}
			a['debit'] = line.amount
			a['partner_id'] = line.partner_id.id if line.partner_id else False
			a['account_id'] = line.account_id.id
			a['analytic_distribution'] = line.analytic_distribution
			a['name'] = line.narration or self.narration
			c = (0, 0, a)
			move_lines.append(c)
		b = {}
		b['credit'] = self.total
		b['account_id'] = self.account_id.id
		b['name'] = self.narration
		d = (0, 0, b)
		move_lines.append(d)
		tax_list = []
		tax_list_id = []
		tax_datails = []
		amount = 0
		for line in self.voucher_line_ids:
			if line.tax:
				if line.tax not in tax_list_id:
					tax_list.append({'tax': line.tax, 'amount': line.tax_amount})
					tax_list_id.append(line.tax)
				else:
					for item in tax_list:
						if item['tax'] == line.tax:
							amount = item['amount'] + line.tax_amount
							tax_list[:] = [d for d in tax_list if d.get('tax') != line.tax]
							tax_list.append({'tax': line.tax, 'amount': amount})
		for element in tax_list:
			tax = element['tax']
			for grp in tax.invoice_repartition_line_ids:
				if grp.repartition_type == 'tax':
					tax_datails.append({'amount': element['amount'], 'account_id': grp.account_id.id})

		for element in tax_datails:
			tax = {}
			tax['debit'] = element['amount']
			tax['account_id'] = element['account_id']
			tax['name'] = self.narration
			d = (0, 0, tax)
			move_lines.append(d)

		move = self.env['account.move'].create({
			'ref': self.name,
			'name': '/',
			'journal_id': self.journal_id.id,
			'date': self.voucher_date,
			'line_ids': move_lines
		})
		move._post()

		if self.name == "New":
			new_name = self.env["ir.sequence"].next_by_code("mx.payment.voucher",sequence_date=self.voucher_date) or _("New")
			self.name = new_name

		self.journal_entry_id = move.id
		self.state = 'post'
	def view_journal_entry(self):
		action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_journal_line")
		form_view = [(self.env.ref('account.view_move_form').id, 'form')]
		action['views'] = form_view
		action['res_id'] = self.journal_entry_id.id
		context = {
			'default_move_type': 'entry',
		}
		action['context'] = context
		return action

class MxVoucherLines(models.Model):
	_name = 'mx.payment.voucher.line'
	_inherit = 'analytic.mixin'
	_description = 'Payment Voucher Line'

	voucher_id = fields.Many2one('mx.payment.voucher', ondelete='cascade')
	account_id = fields.Many2one('account.account')
	partner_id = fields.Many2one('res.partner')
	tax = fields.Many2one('account.tax')
	tax_amount = fields.Float(compute='_get_tax_amount')
	amount = fields.Float()
	analytic_id = fields.Many2one('account.analytic.account')
	narration = fields.Char('Narration')

	@api.depends('amount','tax')
	def _get_tax_amount(self):
		"""Calculation tax amount"""
		for record in self:
			record.tax_amount = 0.0
			if record.tax  and record.amount:
				record.tax_amount = (record.tax.amount/100)*record.amount