{
    "name": "Custom Invoice Report",
    "version": "20.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "",
    "depends": ["account"],
    "data": [ "report/invoice_report.xml",
              "views/res_partner_views.xml",],
    'assets': {
        'web.report_assets_common': [
            'custom_invoice_report/static/src/css/invoice_report.css',
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
