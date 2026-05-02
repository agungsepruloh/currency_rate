from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestPurchaseCurrencyRate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.company_currency = cls.company.currency_id

        cls.foreign_currency = cls.env['res.currency'].search(
            [('id', '!=', cls.company_currency.id), ('active', '=', True)],
            limit=1,
        )
        if not cls.foreign_currency:
            cls.skipTest(cls, "No active foreign currency available")

        cls.partner = cls.env['res.partner'].create({'name': 'Test Vendor'})

    def _create_order(self, currency=None):
        return self.env['purchase.order'].create({
            'partner_id': self.partner.id,
            'currency_id': (currency or self.company_currency).id,
        })

    def test_currencies_are_different_same_currency(self):
        order = self._create_order(self.company_currency)
        self.assertFalse(order.currencies_are_different)

    def test_currencies_are_different_foreign_currency(self):
        order = self._create_order(self.foreign_currency)
        self.assertTrue(order.currencies_are_different)

    def test_company_currency_id_equals_company(self):
        order = self._create_order()
        self.assertEqual(order.company_currency_id, self.company_currency)

    def test_currencies_are_different_recomputes_on_change(self):
        order = self._create_order(self.company_currency)
        self.assertFalse(order.currencies_are_different)
        order.currency_id = self.foreign_currency
        self.assertTrue(order.currencies_are_different)
