from urllib.parse import urlencode

from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.cart.forms import CartAddProductForm

from .models import Category, Product

# Allow-list of sort options: public value -> (label, ordering).
SORT_OPTIONS = {
    "newest": ("Newest arrivals", "-created_at"),
    "price_asc": ("Price: low to high", "price"),
    "price_desc": ("Price: high to low", "-price"),
    "name": ("Name", "name"),
}
DEFAULT_SORT = "newest"


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True).select_related("category")

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    sort = request.GET.get("sort", DEFAULT_SORT)
    if sort not in SORT_OPTIONS:
        sort = DEFAULT_SORT
    products = products.order_by(SORT_OPTIONS[sort][1])

    # TODO: pagination - see TASKS.md (BE-2).

    # Query string that keeps search/sort when switching category.
    params = {}
    if query:
        params["q"] = query
    if sort != DEFAULT_SORT:
        params["sort"] = sort
    filter_qs = f"?{urlencode(params)}" if params else ""

    return render(
        request,
        "catalog/product_list.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
            "query": query,
            "sort": sort,
            "sort_options": [(value, label) for value, (label, _) in SORT_OPTIONS.items()],
            "filter_qs": filter_qs,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(
        request,
        "catalog/product_detail.html",
        {"product": product, "cart_product_form": CartAddProductForm()},
    )
