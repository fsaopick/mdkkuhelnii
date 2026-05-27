from django import forms

from .models import Brand, Cart, CartItem, Category, Order, OrderItem, Product, Review


BASE_INPUT_CLASSES = "form-control"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            current_classes = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{current_classes} {BASE_INPUT_CLASSES}".strip()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = "__all__"


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = "__all__"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = "__all__"
