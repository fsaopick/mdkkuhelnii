from django.contrib import admin

from .models import Brand, Cart, CartItem, Category, Order, OrderItem, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "product_type", "brand", "price", "stock_quantity", "is_exists")
    list_filter = ("product_type", "category", "brand", "is_exists")
    search_fields = ("name", "sku", "description")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author_name", "product", "rating", "is_published", "created_at")
    list_filter = ("rating", "is_published")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("session_key", "created_at")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "customer_phone", "total_price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "customer_phone", "customer_email")
    inlines = [OrderItemInline]
