from odoo import api, fields, models

class XCommissionSettlement(models.Model):
    _name = "x_commission_settlement"
    _description = "Commission Settlement (Simple)"
    _order = "id desc"

    name = fields.Char(required=True, default="New")

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company
    )

    currency_id = fields.Many2one(
        "res.currency",
        required=True,
        default=lambda self: self.env.company.currency_id
    )

    line_ids = fields.One2many(
        "x_commission_settlement_line",
        "settlement_id",
        string="Lines",
    )

    total_commission = fields.Monetary(
        currency_field="currency_id",
        compute="_compute_total_commission",
        store=False,
    )

    def _compute_total_commission(self):
        for rec in self:
            rec.total_commission = sum(rec.line_ids.mapped("commission_amount"))