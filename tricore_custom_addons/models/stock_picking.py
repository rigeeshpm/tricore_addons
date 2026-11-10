from odoo import models, fields


class StockMove(models.Model):
    _inherit = "stock.move"

    remarks = fields.Text()

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    remarks = fields.Text()
