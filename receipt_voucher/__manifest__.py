{
    "name": "Receipt Voucher",
    "version": "20.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "",
    "depends": ["account","sale","purchase","l10n_sa"],
    "data": [
              "security/ir.access.csv",
            "views/receipt_voucher_views.xml",
            "views/sequence.xml",
            "reports/report_receipt_voucher.xml"
              ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
