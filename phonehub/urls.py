from django.urls import path

from .views import (
    add_to_cart_view,
    catalog_view,
    home_view,
    info_view,
    korzina_view,
    orders_view,
    product_create_view,
    product_delete_view,
    product_detail_view,
    product_list_view,
    product_update_view,
    reviews_view,
    update_cart_item_view,
)


urlpatterns = [
    path("", home_view, name="home"),
    path("info/", info_view, name="info"),
    path("catalog/", catalog_view, name="catalog"),
    path("products/", product_list_view, name="products_list"),
    path("product/create/", product_create_view, name="product_create_empty"),
    path("reviews/", reviews_view, name="reviews"),
    path("orders/", orders_view, name="orders"),
    path("cart/", korzina_view, name="cart"),
    path("korzina/", korzina_view, name="korzina"),
    path("cart/add/<int:pk>/", add_to_cart_view, name="add_to_cart"),
    path("cart/item/<int:item_id>/<str:action>/", update_cart_item_view, name="update_cart_item"),
    path("product/<int:pk>/", product_detail_view, name="product_detail"),
    path("product/<int:pk>/create/", product_create_view, name="product_create"),
    path("product/<int:pk>/update/", product_update_view, name="product_update"),
    path("product/<int:pk>/delete/", product_delete_view, name="product_delete"),
]
