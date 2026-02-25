from odoo import fields, models

class XCommissionSettlementLine(models.Model):
    _name = "x_commission_settlement_line"
    _description = "Commission Settlement Line (Simple)"
    _order = "id desc"

    settlement_id = fields.Many2one(
        "x_commission_settlement",
        required=True,
        ondelete="cascade",
    )

    agent_id = fields.Many2one(
        "res.partner",
        string="Agent",
        required=True,
    )

    invoice_id = fields.Many2one(
        "account.move",
        string="Invoice",
    )

    commission_amount = fields.Monetary(
        currency_field="currency_id",
        required=True,
        default=0.0,
    )

    currency_id = fields.Many2one(
        "res.currency",
        related="settlement_id.currency_id",
        store=True,
        readonly=True,
    )