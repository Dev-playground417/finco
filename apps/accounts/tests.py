from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegistrationTests(TestCase):
    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "bob",
                "email": "bob@example.com",
                "password1": "V3ry-Str0ng-pass",
                "password2": "V3ry-Str0ng-pass",
            },
        )
        self.assertRedirects(response, reverse("catalog:product_list"))
        self.assertTrue(get_user_model().objects.filter(username="bob").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_page_renders(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
