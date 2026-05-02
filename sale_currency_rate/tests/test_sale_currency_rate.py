from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestSaleCurrencyRate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.company_currency = cls.company.currency_id

        cls.foreign_currency = cls.env['res.currency'].search(
            [('id', '!=', cls.company_currency.id), ('active', '=', True)],
            limit=1,
        )
        cls.partner = cls.env['res.partner'].create({'name': 'Test Customer'})

        # Explicit pricelists so tests don't depend on DB default pricelist
        cls.company_pricelist = cls.env['product.pricelist'].create({
            'name': 'Test Company Pricelist',
            'currency_id': cls.company_currency.id,
        })
        if cls.foreign_currency:
            cls.foreign_pricelist = cls.env['product.pricelist'].create({
                'name': 'Test Foreign Pricelist',
                'currency_id': cls.foreign_currency.id,
            })
        else:
            cls.foreign_pricelist = False

    def _create_order(self, pricelist=None):
        return self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'pricelist_id': (pricelist or self.company_pricelist).id,
        })

    def test_currencies_are_different_same_currency(self):
        order = self._create_order(self.company_pricelist)
        self.assertEqual(order.currency_id, self.company_currency)
        self.assertFalse(order.currencies_are_different)

    def test_currencies_are_different_foreign_currency(self):
        if not self.foreign_currency:
            self.skipTest("No active foreign currency available")
        order = self._create_order(self.foreign_pricelist)
        self.assertEqual(order.currency_id, self.foreign_currency)
        self.assertTrue(order.currencies_are_different)

    def test_company_currency_id_equals_company(self):
        order = self._create_order(self.company_pricelist)
        self.assertEqual(order.company_currency_id, self.company_currency)

    def test_currencies_are_different_recomputes_on_change(self):
        if not self.foreign_currency:
            self.skipTest("No active foreign currency available")
        order = self._create_order(self.company_pricelist)
        self.assertFalse(order.currencies_are_different)
        order.pricelist_id = self.foreign_pricelist
        self.assertTrue(order.currencies_are_different)
