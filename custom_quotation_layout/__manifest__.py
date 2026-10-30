{
    "name": "Custom Quotation Layout",
    "version": "20.0.0.1",
    "category": "Sales",
    "summary": "Custom quotation details table and Terms and Conditions page",
    "depends": ["sale", "web","custom_report_page_layout"],
    "data": ["views/report_saleorder_templates.xml"],
    'assets': {
        'web.report_assets_common': [
            'custom_quotation_layout/static/src/css/sales_quotation_layout.css',
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
