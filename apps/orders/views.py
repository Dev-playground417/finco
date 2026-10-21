from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.cart.cart import Cart

from .forms import OrderCreateForm


@login_required
def order_create(request):
    cart = Cart(request)
    if not len(cart):
        messages.info(request, "Your cart is empty.")
        return redirect("cart:cart_detail")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # TODO (TASKS.md BE-4): create the Order and its OrderItems from the cart,
            # update stock, clear the cart and redirect to a confirmation page.
            messages.warning(request, "Checkout is not implemented yet.")
            return redirect("orders:order_create")
    else:
        form = OrderCreateForm(
            initial={"full_name": request.user.get_full_name(), "email": request.user.email}
        )

    return render(request, "orders/create.html", {"cart": cart, "form": form})
