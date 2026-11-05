from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    note = fields.Html(
        string='Terms and Conditions',
        default="""
                        <ol style="padding-left: 20px; margin: 0;">
                <li style="margin-bottom: 10px;">
                    <strong>Quotation Validity</strong><br/>
                    This quotation is valid for the period mentioned in the quotation.
                    Prices and availability may change after the validity period.
                </li>
                <li style="margin-bottom: 10px;">
                    <strong>Prices</strong><br/>
                    All prices are quoted in Saudi Riyals (SAR) and are exclusive/inclusive
                    of VAT as specifically stated in the quotation.
                </li>
                <li style="margin-bottom: 10px;">
                    <strong>Order Confirmation</strong><br/>
                    Orders will be processed only upon receipt of an official Purchase Order (PO)
                    or written confirmation from the customer.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Payment Terms</strong><br/>
                    Payment shall be made according to the agreed payment terms mentioned in
                    the quotation. Any additional charges resulting from delayed payment may be applicable.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Delivery</strong><br/>
                    Delivery timelines are estimated and may vary depending on product availability,
                    supplier lead time, customs clearance, transportation, or other circumstances
                    beyond our control.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Product Availability</strong><br/>
                    Product availability is subject to confirmation at the time of order.
                    Items may be subject to prior sale.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Changes &amp; Cancellation</strong><br/>
                    Any cancellation or modification of an order after confirmation may be subject
                    to applicable charges, depending on the order status and supplier terms.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Warranty</strong><br/>
                    Warranty, where applicable, will be provided according to the manufacturer's
                    standard warranty terms. Warranty does not cover damage resulting from misuse,
                    improper installation, unauthorized repair, or normal wear and tear.
                </li>
                <li style="margin-bottom: 10px;">
                    <strong>Installation &amp; Services</strong><br/>
                    Installation, configuration, testing, commissioning, transportation, or other
                    services will be provided only if specifically mentioned in the quotation.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Taxes &amp; Government Charges</strong><br/>
                    VAT and any applicable government fees, customs duties, clearance charges,
                    or other statutory charges will be charged as applicable unless otherwise stated.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Inspection &amp; Acceptance</strong><br/>
                    The customer shall inspect the delivered items upon receipt and notify us of
                    any visible shortage or damage within the agreed period.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Force Majeure</strong><br/>
                    The company shall not be liable for delays or failure to perform due to
                    circumstances beyond its reasonable control, including supplier delays,
                    transportation issues, customs restrictions, natural disasters, government
                    regulations, or other unforeseen events.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Ownership of Goods</strong><br/>
                    Ownership of the supplied goods shall remain with the company until full
                    payment has been received, where applicable under the agreed payment terms.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Quotation Scope</strong><br/>
                    Only the items, quantities, specifications, and services specifically
                    mentioned in the quotation are included. Any additional requirements
                    will be quoted separately.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Customer Responsibilities</strong><br/>
                    The customer shall provide necessary site access, approvals, permits,
                    information, and other requirements needed to complete the order or
                    service, where applicable.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Technical Specifications</strong><br/>
                    Product specifications are subject to the manufacturer's latest standards.
                    Equivalent or upgraded models may be offered subject to availability
                    and customer approval.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Validity of Agreement</strong><br/>
                    By issuing a Purchase Order or written confirmation, the customer
                    acknowledges and accepts the quotation, specifications, payment terms,
                    and conditions stated herein.
                </li>

                <li style="margin-bottom: 10px;">
                    <strong>Governing Law</strong><br/>
                    These terms and conditions shall be governed by and interpreted in
                    accordance with the applicable laws and regulations of the Government.
                </li>
            </ol>

        """,
    )
