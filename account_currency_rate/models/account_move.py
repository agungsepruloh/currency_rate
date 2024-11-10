from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    currencies_are_different = fields.Boolean(
        string="Currencies are different",
        compute='_compute_currencies_are_different',
        help="Utility field to express if the currency of the sale order is different from the company currency"
    )
    currency_rate = fields.Float(
        compute='_compute_currency_rate',
        help="Currency rate from company currency to document currency.",
    )

    @api.depends('currency_id', 'company_currency_id')
    def _compute_currencies_are_different(self):
        for order in self:
            order.currencies_are_different = order.currency_id != order.company_currency_id

    @api.depends('currency_id', 'company_currency_id', 'invoice_date', 'date')
    def _compute_currency_rate(self):
        for move in self:
            if move.currency_id:
                move.currency_rate = self.env['res.currency']._get_conversion_rate(
                    from_currency=move.company_currency_id,
                    to_currency=move.currency_id,
                    company=move.company_id,
                    date=move.invoice_date or move.date or fields.Date.context_today(move),
                )
            else:
                move.currency_rate = 1

