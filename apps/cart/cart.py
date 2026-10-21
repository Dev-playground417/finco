import copy
from decimal import Decimal

from django.conf import settings

from apps.catalog.models import Product


class Cart:
    """Shopping cart stored in the user's session.

    Session layout: {"<product_id>": {"quantity": int, "price": "<decimal str>"}}
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if cart is None:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Add a product to the cart, or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart or override_quantity:
            self.cart[product_id] = {"quantity": quantity, "price": str(product.price)}
        else:
            self.cart[product_id]["quantity"] = quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        """Yield cart items with their Product instance and line totals attached."""
        products = Product.objects.filter(id__in=self.cart.keys())
        cart = copy.deepcopy(self.cart)
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Total number of units in the cart."""
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            (Decimal(item["price"]) * item["quantity"] for item in self.cart.values()),
            Decimal("0.00"),
        )
