{
    "name": "Payment Voucher Tricore",
    "version": "20.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "",
    "depends": ["account","sale","l10n_sa"],
    "data": [
                "security/ir.access.csv",
              "views/payment_voucher_views.xml",
              ],
    'assets': {
        'web.report_assets_common': [
            'tricore_custom_addons/static/src/css/styles.css',
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
