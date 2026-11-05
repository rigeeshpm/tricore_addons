from odoo import fields, models


from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    note = fields.Html(
        string='Terms and Conditions',
        default="""
            <ul style="padding-left: 15px; margin-bottom: 0;">
                <li>
                    All request delivery dates refer to the receiving
                    of the goods at Tricore Trading or the mention
                    place of delivery.
                </li>
                <li>
                    Invoice and delivery notes must refer to our
                    purchase order number and sent to our finance
                    department / finance@tricore.com within
                    5 working days.
                </li>
                <li>
                    Invoice addressed incorrectly will not be
                    considered for payment processing.
                </li>
                <li>
                    Invoice date cannot be earlier than the delivery
                    date. Also attach the copy of delivery note duly
                    signed by an authorized person.
                </li>
                <li>
                    Please notify us immediately if you are unable
                    to ship as specified. We reserve the right to
                    cancel the order if the delivery is delayed
                    above the agreed date.
                </li>
                <li>
                    Quantity &amp; items delivered other than those
                    specified above either will not be accepted by
                    us or will be returned to the vendor. All
                    transportation, freight and other incidental
                    cost related to the returned material will be
                    borne by the vendor.
                </li>
            </ul>
        """,
    )
