from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import Category, Product


class CartViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Sports", slug="sports")
        cls.product = Product.objects.create(
            category=category,
            name="Yoga Mat",
            slug="yoga-mat",
            price=Decimal("24.99"),
            cost_price=Decimal("8.10"),
            stock=10,
        )

    def add(self, quantity, override=False):
        data = {"quantity": quantity}
        if override:
            data["override"] = "True"
        return self.client.post(reverse("cart:cart_add", args=[self.product.id]), data)

    def test_add_product(self):
        response = self.add(2)
        self.assertRedirects(response, reverse("cart:cart_detail"))
        cart = self.client.session["cart"]
        self.assertEqual(cart[str(self.product.id)]["quantity"], 2)

    def test_override_quantity(self):
        self.add(2)
        self.add(5, override=True)
        cart = self.client.session["cart"]
        self.assertEqual(cart[str(self.product.id)]["quantity"], 5)

    def test_remove_product(self):
        self.add(1)
        self.client.post(reverse("cart:cart_remove", args=[self.product.id]))
        self.assertEqual(self.client.session["cart"], {})

    def test_cart_detail_shows_total(self):
        self.add(2)
        response = self.client.get(reverse("cart:cart_detail"))
        self.assertContains(response, "49.98")

    def test_cart_detail_renders_quantity_form(self):
        self.add(2)
        response = self.client.get(reverse("cart:cart_detail"))
        self.assertContains(response, '<option value="2" selected>', html=False)

    def test_add_requires_post(self):
        response = self.client.get(reverse("cart:cart_add", args=[self.product.id]))
        self.assertEqual(response.status_code, 405)
