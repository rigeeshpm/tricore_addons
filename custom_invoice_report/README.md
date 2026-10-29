# Invoice Client Details Table — Odoo 20

## Included
- Client Details title row spanning the full table.
- English customer name and Arabic customer name.
- Address row with English street, city, and state/province, plus Arabic street, city, state/province, and country.
- Arabic fields added to the Contact form.
- QWeb report inheritance; no Odoo core files are edited.

## Install
1. Extract `odoo20_invoice_client_details` into a directory included in `addons_path`.
2. Restart Odoo.
3. Enable Developer Mode, update the Apps list, and install **Invoice Client Details Table**.
4. Open the relevant contact records and fill in the new Arabic fields.
5. Print a customer invoice PDF and verify the result.

CLI alternative (adjust database and paths):
`./odoo-bin -d YOUR_DATABASE -u odoo20_invoice_client_details --stop-after-init`

## Layout assumptions
The request described eight columns in row 3 but did not specify the eighth column. This module assumes:
1. Street label
2. English street
3. English city
4. English state/province
5. Arabic street
6. Arabic city
7. Arabic state/province
8. Arabic country

Column widths follow the requested grouping: column 1 matches the row-2 label width; columns 2–4 together match the row-2 English-name cell width; columns 5–7 together match the row-2 Arabic-label cell width; column 8 uses the remaining 25%.

The XPath and view anchors are based on the standard Odoo invoice report and partner form and should be tested against your exact Odoo 20 build and any installed localization/custom modules. Test on a staging database before production use.
