from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class CheckoutAccessTests(TestCase):
    def test_checkout_requires_login(self):
        url = reverse("orders:order_create")
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={url}")

    def test_empty_cart_redirects_to_cart(self):
        user = get_user_model().objects.create_user("alice", password="S3cure-pass!")
        self.client.force_login(user)
        response = self.client.get(reverse("orders:order_create"))
        self.assertRedirects(response, reverse("cart:cart_detail"))
