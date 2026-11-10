from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    _order = "code"
    _rec_names_search = ("complete_name", "email", "ref", "vat", "code")

    code = fields.Char(string="Code", copy=False, readonly=True)
    _code_unique = models.Constraint(
        "unique(code)",
        "Code already exists!",
    )

    @api.depends("code")
    def _compute_display_name(self):
        super()._compute_display_name()
        for partner in self:
            if partner.code:
                partner.display_name = f"{partner.code} - {partner.display_name}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code"):
                continue
            if self.env.context.get("default_customer_rank", 0) > 0:
                vals["code"] = self.env["ir.sequence"].next_by_code(
                    "res.partner.customer.sequence"
                )
            elif self.env.context.get("default_supplier_rank", 0) > 0:
                vals["code"] = self.env["ir.sequence"].next_by_code(
                    "res.partner.vendor.sequence"
                )
            else:
                vals["code"] = self.env["ir.sequence"].next_by_code(
                    "res.partner.customer.sequence"
                )
                vals["customer_rank"] = 1
        return super().create(vals_list)

    @api.model
    def generate_partner_sequence(self, records):
        """Assign a customer or vendor sequence to partners that still have no code."""
        for record in records:
            if record.code and record.code != "New":
                continue
            sequence_code = False
            if record.customer_rank > 0 or record.parent_id.customer_rank > 0:
                sequence_code = "res.partner.customer.sequence"
            elif record.supplier_rank > 0 or record.parent_id.supplier_rank > 0:
                sequence_code = "res.partner.vendor.sequence"
            if sequence_code:
                record.code = self.env["ir.sequence"].next_by_code(sequence_code)
