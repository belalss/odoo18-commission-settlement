{
    "name": "Commission Settlement Wizard (Odoo 18)",
    "version": "18.0.1.0.0",
    "category": "Sales/Commissions",
    "summary": "Generate commission settlements from paid invoices (OCA commissions on Odoo 18).",
    "depends": [
    "account",
    "commission_oca",
    "sale_commission_oca",
    "account_commission_oca",
],
    "data": [
    "security/ir.model.access.csv",

    # actions + views first
    "views/settlement_views.xml",
    "views/wizard_views.xml",

    # menu last (menus reference actions)
    "views/menu.xml",
],
    "installable": True,
    "application": False,
}