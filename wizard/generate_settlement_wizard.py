from odoo import fields, models, _
from odoo.exceptions import UserError

class XCommissionSettlementGenerateWizard(models.TransientModel):
    _name = "x_commission_settlement_generate_wizard"
    _description = "Generate Commission Settlement (Simple)"

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    def action_generate(self):
        self.ensure_one()

        # 1) Find paid customer invoices in range
        invoices = self.env["account.move"].search([
            ("move_type", "=", "out_invoice"),
            ("invoice_date", ">=", self.date_from),
            ("invoice_date", "<=", self.date_to),
            ("payment_state", "=", "paid"),
        ])

        if not invoices:
            raise UserError(_("No paid invoices found in this date range."))

        # 2) Create settlement header
        settlement = self.env["x_commission_settlement"].create({
            "name": "Settlement",
            "date_from": self.date_from,
            "date_to": self.date_to,
        })

        # 3) Build settlement lines from invoice line agent rows
        lines_to_create = []
        for inv in invoices:
            for inv_line in inv.invoice_line_ids:
                # OCA: agent lines are on invoice line
                for agent_line in inv_line.agent_ids:
                    amount = agent_line.amount or 0.0
                    if amount <= 0:
                        continue

                    # agent_line.agent_id should exist in your system
                    lines_to_create.append({
                        "settlement_id": settlement.id,
                        "agent_id": agent_line.agent_id.id,
                        "invoice_id": inv.id,
                        "commission_amount": amount,
                    })

        if not lines_to_create:
            raise UserError(_("Paid invoices found, but none has agent commission lines."))

        self.env["x_commission_settlement_line"].create(lines_to_create)

        # 4) Open the settlement
        return {
            "type": "ir.actions.act_window",
            "res_model": "x_commission_settlement",
            "view_mode": "form",
            "res_id": settlement.id,
            "target": "current",
        }