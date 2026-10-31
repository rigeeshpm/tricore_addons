{
    "name": "Custom Addons for Tricore",
    "version": "20.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "",
    "depends": ["account","sale","sale_stock"],
    "data": [ "report/templates.xml",
             "report/invoice_report.xml",
              "report/report_saleorder_templates.xml",
              "views/res_partner_views.xml",],
    'assets': {
        'web.report_assets_common': [
            'tricore_custom_addons/static/src/css/styles.css',
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
