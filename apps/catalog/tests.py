from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class CatalogTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Books", slug="books")
        cls.product = Product.objects.create(
            category=cls.category,
            name="Fluent Python",
            slug="fluent-python",
            price=Decimal("54.99"),
            cost_price=Decimal("30.00"),
            stock=5,
        )
        cls.hidden = Product.objects.create(
            category=cls.category,
            name="Retired Book",
            slug="retired-book",
            price=Decimal("10.00"),
            cost_price=Decimal("5.00"),
            is_active=False,
        )


class ProductViewTests(CatalogTestCase):
    def test_product_list_shows_active_products_only(self):
        response = self.client.get(reverse("catalog:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fluent Python")
        self.assertNotContains(response, "Retired Book")

    def test_product_list_filters_by_category(self):
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["products"]), [self.product])

    def test_product_detail(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "54.99")

    def test_inactive_product_detail_returns_404(self):
        response = self.client.get(self.hidden.get_absolute_url())
        self.assertEqual(response.status_code, 404)


class ProductApiTests(CatalogTestCase):
    def test_list_products(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_retrieve_product_by_slug(self):
        response = self.client.get("/api/products/fluent-python/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Fluent Python")
