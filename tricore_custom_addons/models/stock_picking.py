from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    note = fields.Html(
        string='Terms and Conditions',
        default="""
                                           <ul style="padding-left:25px; margin-top:12px;">

                        <li style="padding-bottom:3px;">
                            Return of received materials shall be allowed
                            to authorized approvals and issuance of return voucher.
                        </li>

                        <li style="padding-bottom:3px;">
                            Payment terms are applicable from the date of
                            delivery of materials. Failing to comply with
                            the above mentioned payment terms will be
                            automatic suspension of your credit facility with us.
                        </li>

                        <li style="padding-bottom:3px;">
                            Any discrepancy related to this delivery should
                            be reported to store sales@tricoretrading.com
                            within 24 hours from the time &amp; date of receipt
                            of materials. After this cut-off time, this delivery
                            will be considered as your confirmation of acceptance.
                        </li>
                    </ul>

        """,
    )

class StockMove(models.Model):
    _inherit = "stock.move"

    remarks = fields.Text()

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    remarks = fields.Text()
