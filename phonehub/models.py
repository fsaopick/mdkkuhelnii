from django.db import models
from django.utils.text import slugify


MAX_LENGTH = 255


class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name="Название сегмента")
    description = models.TextField(null=True, blank=True, verbose_name="Описание сегмента")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сегмент"
        verbose_name_plural = "Сегменты"
        ordering = ["name"]


class Brand(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name="Название бренда")
    description = models.TextField(null=True, blank=True, verbose_name="Описание бренда")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ["name"]


class Product(models.Model):
    class ProductType(models.TextChoices):
        FLAGSHIP = "flagship", "Флагман"
        CAMERA = "camera", "Камерофон"
        FOLDABLE = "foldable", "Складной"
        GAMING = "gaming", "Игровой"
        BUDGET = "budget", "Доступный"

    name = models.CharField(max_length=MAX_LENGTH, verbose_name="Название смартфона")
    slug = models.SlugField(max_length=MAX_LENGTH, unique=True, blank=True, verbose_name="Слаг")
    sku = models.CharField(max_length=64, unique=True, verbose_name="Артикул")
    product_type = models.CharField(max_length=20, choices=ProductType.choices, verbose_name="Тип смартфона")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="Сегмент")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="products", verbose_name="Бренд")
    description = models.TextField(null=True, blank=True, verbose_name="Описание смартфона")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    color = models.CharField(max_length=100, blank=True, verbose_name="Цвет")
    photo = models.ImageField(upload_to="phones/%Y/%m/%d", null=True, blank=True, verbose_name="Фото")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")
    is_exists = models.BooleanField(default=True, verbose_name="Доступен к продаже")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлен")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.price} ₽"

    class Meta:
        verbose_name = "Смартфон"
        verbose_name_plural = "Смартфоны"
        ordering = ["name"]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="Смартфон")
    author_name = models.CharField(max_length=150, verbose_name="Имя автора")
    email = models.EmailField(blank=True, verbose_name="Email")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка")
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")

    def __str__(self):
        return f"{self.author_name} - {self.product.name}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]


class Cart(models.Model):
    session_key = models.CharField(max_length=64, unique=True, verbose_name="Ключ сессии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Корзина {self.session_key}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items", verbose_name="Смартфон")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новый"
        PROCESSING = "processing", "В обработке"
        COMPLETED = "completed", "Завершен"

    customer_name = models.CharField(max_length=150, verbose_name="Имя покупателя")
    customer_email = models.EmailField(verbose_name="Email")
    customer_phone = models.CharField(max_length=30, verbose_name="Телефон")
    city = models.CharField(max_length=100, blank=True, verbose_name="Город")
    street = models.CharField(max_length=150, blank=True, verbose_name="Улица")
    house = models.CharField(max_length=30, blank=True, verbose_name="Дом")
    apartment = models.CharField(max_length=30, blank=True, verbose_name="Квартира")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Сумма заказа")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Заказ #{self.pk}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_items", verbose_name="Смартфон")
    product_name = models.CharField(max_length=MAX_LENGTH, verbose_name="Название смартфона")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
