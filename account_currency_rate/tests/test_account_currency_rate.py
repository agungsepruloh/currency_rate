from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestAccountCurrencyRate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.company_currency = cls.company.currency_id

        cls.foreign_currency = cls.env['res.currency'].search(
            [('id', '!=', cls.company_currency.id), ('active', '=', True)],
            limit=1,
        )
        cls.partner = cls.env['res.partner'].create({'name': 'Test Partner'})

    def _create_invoice(self, currency=None):
        return self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'currency_id': (currency or self.company_currency).id,
        })

    def test_currencies_are_different_same_currency(self):
        invoice = self._create_invoice(self.company_currency)
        self.assertFalse(invoice.currencies_are_different)

    def test_currencies_are_different_foreign_currency(self):
        if not self.foreign_currency:
            self.skipTest("No active foreign currency available")
        invoice = self._create_invoice(self.foreign_currency)
        self.assertTrue(invoice.currencies_are_different)

    def test_currency_rate_same_currency(self):
        invoice = self._create_invoice(self.company_currency)
        self.assertEqual(invoice.currency_rate, 1.0)

    def test_currency_rate_foreign_currency_positive(self):
        if not self.foreign_currency:
            self.skipTest("No active foreign currency available")
        invoice = self._create_invoice(self.foreign_currency)
        self.assertGreater(invoice.currency_rate, 0)

    def test_currency_rate_recomputes_on_currency_change(self):
        if not self.foreign_currency:
            self.skipTest("No active foreign currency available")
        invoice = self._create_invoice(self.company_currency)
        self.assertFalse(invoice.currencies_are_different)
        invoice.currency_id = self.foreign_currency
        self.assertTrue(invoice.currencies_are_different)
        self.assertGreater(invoice.currency_rate, 0)
