from django.db import models
from django.conf import settings
from django.db.models import Sum, F, ExpressionWrapper


class Product(models.Model):
    SUHIE = 'сухие смеси и грунтовки'
    LISTOVIE = 'Листовые материалы'
    OBLICOV = 'Облицовочные материалы'
    ISOL = 'Изоляционные материалы'

    CHOICE_GROUP = {
        (SUHIE, 'сухие смеси и грунтовки'),
        (LISTOVIE, 'Листовые материалы'),
        (OBLICOV, 'Облицовочные материалы'),
        (ISOL, 'Изоляционные материалы'),
    }

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    available_count = models.IntegerField(default=1, verbose_name='Количество')
    group = models.CharField(max_length=50, choices=CHOICE_GROUP, default=SUHIE)
    img = models.ImageField(default='no_image.jpg', upload_to='product_image')

    @property
    def availability(self):
        return self.available_count != 0

    def __str__(self):
        return f'{self.name} ({self.available_count})'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Cart(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Клиент', on_delete=models.CASCADE)

    @property
    def price(self):
        aggregate = self.cartentry_set.aggregate(
            price=ExpressionWrapper(Sum('product__price') * F('count'), output_field=models.PositiveIntegerField())
        )
        prics = aggregate.get('price', 0) or 0
        return prics

    def __str__(self):
        return f'{str(self.created_by)} - [{str(self.cartentry_set.count())}]'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'


class CartEntry(models.Model):
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT, verbose_name='Товар')
    count = models.PositiveIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f'{str(self.product)} ({str(self.count)})'

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'


class Pay(models.Model):
    cart_id = models.ForeignKey(Cart, verbose_name='Корзина', related_name='cart', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Клиент', on_delete=models.CASCADE)
    fullName = models.CharField(max_length=255, default='User FF', verbose_name='ФИО клиента')
    number = models.CharField(max_length=22, verbose_name='Телефон номер')
    address = models.CharField(max_length=255, verbose_name='')
    pay = models.PositiveIntegerField(default=0, verbose_name='Тип оплаты',
                                      choices={(0, u'Наличные'), (1, u'Оплата картой')})
    delivery = models.PositiveIntegerField(default=0, verbose_name='Стоимость доставки')

    def __str__(self):
        return str(self.created_by)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказов'
