from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    currencies_are_different = fields.Boolean(
        string="Currencies are different",
        compute='_compute_currencies_are_different',
        help="Utility field to express if the currency of the purchase order is different from the company currency"
    )

    @api.depends('currency_id', 'company_currency_id')
    def _compute_currencies_are_different(self):
        for order in self:
            order.currencies_are_different = order.currency_id != order.company_currency_id
