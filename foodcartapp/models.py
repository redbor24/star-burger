from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


def order_mum_default():
    return '1'


class OrderQuerySet(models.QuerySet):
    def get_order_amount(self):
        return self.annotate(amount=Sum(F('lines__quantity') * F('lines__price')))


class Order(models.Model):
    ORDER_STATUS = (
        ('u', 'Необработанный'),
        ('p', 'Обработанный'),
    )
    order_num = models.CharField(max_length=255, verbose_name='Номер заказа', default=order_mum_default)
    first_name = models.CharField(max_length=255, verbose_name='Имя заказчика', db_index=True)
    last_name = models.CharField(max_length=255, verbose_name='Фамилия заказчика', db_index=True)
    phone_number = PhoneNumberField(verbose_name='Телефон', db_index=True)
    delivery_address = models.TextField(verbose_name='Адрес заказа')
    created_at = models.DateTimeField(verbose_name='Дата и время создания заказа', auto_now_add=True)
    status = models.CharField(verbose_name='Статус', max_length=1, choices=ORDER_STATUS, default='u', db_index=True)

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.id}, {self.last_name} {self.first_name}, {self.phone_number}, {self.delivery_address}"

    @classmethod
    def get_new_order_num(cls):
        return Order.objects.count() + 1


class OrderLines(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='lines', db_index=True,
                              on_delete=models.CASCADE)
    position_num = models.IntegerField(verbose_name='Номер позиции', default=1)
    product = models.ForeignKey(Product, verbose_name='Позиция', related_name='order_lines', db_index=True,
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество, шт.', default=1,
                                   validators=[MinValueValidator(1)])
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2, default=0,
                                validators=[MinValueValidator(1, 'Цена должна быть больше 0')])

    class Meta:
        verbose_name = 'Позиции заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f"заказ: {self.order.order_num}, №{self.position_num}, {self.product}, кол-во: {self.quantity}"
