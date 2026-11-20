from odoo import models, fields

class StockPicking(models.Model):
    _inherit = "stock.picking"

    incoterm_id = fields.Many2one('account.incoterms',string='Delivery Terms',related='sale_id.incoterm')
    incoterm_location = fields.Char("Delivery Location",related="sale_id.incoterm_location")
    region = fields.Char("Region",related="sale_id.project_location")


class StockMove(models.Model):
    _inherit = "stock.move"

    remarks = fields.Text()


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    remarks = fields.Text()
