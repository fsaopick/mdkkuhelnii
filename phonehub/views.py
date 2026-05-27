from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Cart, CartItem, Order, Product, Review


def home_view(request):
    featured_products = Product.objects.filter(is_exists=True).select_related("brand", "category")[:3]
    context = {
        "featured_products": featured_products,
        "products_count": Product.objects.filter(is_exists=True).count(),
        "brands_count": Product.objects.exclude(brand__isnull=True).values("brand").distinct().count(),
        "reviews_count": Review.objects.filter(is_published=True).count(),
        "active_page": "home",
    }
    return render(request, "info.html", context)


def info_view(request):
    return home_view(request)


def catalog_view(request):
    products = Product.objects.filter(is_exists=True).select_related("brand", "category")
    return render(request, "catalog.html", {"products": products, "active_page": "catalog"})


def product_list_view(request):
    products = Product.objects.select_related("brand", "category").all()
    return render(request, "products/products_list.html", {"products": products, "active_page": "products"})


def reviews_view(request):
    reviews = Review.objects.filter(is_published=True).select_related("product", "product__brand")
    return render(request, "reviews.html", {"reviews": reviews, "active_page": "reviews"})


def orders_view(request):
    orders = Order.objects.prefetch_related("items").all()
    return render(request, "orders.html", {"orders": orders, "active_page": "orders"})


def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def korzina_view(request):
    cart = get_or_create_cart(request)
    item_rows = []
    total_price = 0
    total_quantity = 0

    for item in cart.items.select_related("product"):
        row_total = item.product.price * item.quantity
        total_price += row_total
        total_quantity += item.quantity
        item_rows.append({"item": item, "product": item.product, "row_total": row_total})

    return render(
        request,
        "korzina.html",
        {
            "item_rows": item_rows,
            "total_price": total_price,
            "total_quantity": total_quantity,
            "active_page": "cart",
        },
    )


def add_to_cart_view(request, pk):
    product = get_object_or_404(Product, pk=pk, is_exists=True)
    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect("cart")


def update_cart_item_view(request, item_id, action):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)

    if action == "plus":
        item.quantity += 1
        item.save()
    elif action == "minus":
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    elif action == "remove":
        item.delete()

    return redirect("cart")


def product_detail_view(request, pk):
    product = get_object_or_404(Product.objects.select_related("brand", "category"), pk=pk)
    return render(request, "products/products_detail.html", {"product": product, "active_page": "catalog"})


def product_create_view(request, pk=None):
    source_product = None
    if pk is not None:
        source_product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("catalog")
    else:
        if source_product is not None:
            form = ProductForm(
                initial={
                    "product_type": source_product.product_type,
                    "category": source_product.category,
                    "brand": source_product.brand,
                    "color": source_product.color,
                    "is_exists": source_product.is_exists,
                }
            )
        else:
            form = ProductForm()

    return render(
        request,
        "products/products_form.html",
        {
            "form": form,
            "title": "Добавление смартфона",
            "source_product": source_product,
            "active_page": "products",
        },
    )


def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("catalog")
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "products/products_form.html",
        {
            "form": form,
            "title": "Редактирование смартфона",
            "product": product,
            "active_page": "products",
        },
    )


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("catalog")

    return render(
        request,
        "products/products_confirm_delete.html",
        {"product": product, "active_page": "products"},
    )
