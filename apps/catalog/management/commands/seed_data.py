from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from apps.catalog.models import Category, Product

# category -> [(name, price, cost_price, stock), ...]
CATALOG = {
    "Electronics": [
        ("Wireless Headphones", "89.99", "41.00", 25),
        ("Bluetooth Speaker", "49.50", "22.10", 40),
        ("USB-C Charger 65W", "34.99", "12.40", 0),
        ("Mechanical Keyboard", "119.00", "58.75", 12),
        ("4K Webcam", "79.00", "35.20", 7),
    ],
    "Books": [
        ("Fluent Python", "54.99", "30.00", 15),
        ("Two Scoops of Django", "39.95", "18.50", 9),
        ("Clean Architecture", "32.00", "15.00", 3),
        ("The Pragmatic Programmer", "44.90", "21.30", 0),
    ],
    "Home & Kitchen": [
        ("Pour-Over Coffee Set", "29.99", "11.20", 30),
        ("Cast Iron Skillet", "37.50", "16.80", 18),
        ("Bamboo Cutting Board", "19.99", "6.40", 50),
        ("Electric Kettle", "42.00", "19.90", 6),
    ],
    "Sports": [
        ("Yoga Mat", "24.99", "8.10", 35),
        ("Adjustable Dumbbells", "149.00", "82.00", 4),
        ("Running Water Bottle", "14.50", "4.20", 60),
        ("Resistance Bands Set", "21.00", "7.50", 0),
    ],
}

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "DemoPass!2026"


class Command(BaseCommand):
    help = "Populate the database with sample categories, products and a demo customer."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset", action="store_true", help="Delete existing products and categories first."
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            Product.objects.all().delete()
            Category.objects.all().delete()

        created_count = 0
        for category_name, items in CATALOG.items():
            category, _ = Category.objects.get_or_create(
                slug=slugify(category_name),
                defaults={
                    "name": category_name,
                    "description": f"All things {category_name.lower()}.",
                },
            )
            for name, price, cost, stock in items:
                _, created = Product.objects.get_or_create(
                    slug=slugify(name),
                    defaults={
                        "category": category,
                        "name": name,
                        "description": f"{name} - a customer favourite in {category_name}.",
                        "price": Decimal(price),
                        "cost_price": Decimal(cost),
                        "stock": stock,
                    },
                )
                created_count += created

        User = get_user_model()
        if not User.objects.filter(username=DEMO_USERNAME).exists():
            User.objects.create_user(DEMO_USERNAME, "demo@example.com", DEMO_PASSWORD)
            self.stdout.write(f"Created demo user '{DEMO_USERNAME}' / '{DEMO_PASSWORD}'.")

        self.stdout.write(self.style.SUCCESS(f"Seed complete: {created_count} new products."))
