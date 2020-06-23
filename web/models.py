from django.db import models
from django.conf import settings


class Product(models.Model):
    MOBILE = 'mobile'
    NOTEBOOK = 'notebook'
    PC = 'pc'
    ACC = 'accessories'

    CHOICE_GROUP = {
        (MOBILE, 'mobile'),
        (NOTEBOOK, 'notebook'),
        (PC, 'pc'),
        (ACC, 'accessories'),
    }

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    availability = models.BooleanField()
    group = models.CharField(max_length=20, choices=CHOICE_GROUP, default=MOBILE)
    img = models.ImageField(default='no_image.jpg', upload_to='product_image')

    def __str__(self):
        return f'{self.name}'


    class Meta:
        verbose_name='Товар'
        verbose_name_plural='Товары'

class Cart(models.Model):
    product_id = models.ManyToManyField(Product, verbose_name='Товар', related_name='products')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Клиент', on_delete=models.CASCADE)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name='Корзина'
        verbose_name_plural='Корзины'

class Pay(models.Model):
    cart_id = models.ForeignKey(Cart, verbose_name='Корзина', related_name='cart', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Клиент', on_delete=models.CASCADE)
    fullName = models.CharField(max_length=255, default='User FF', verbose_name='ФИО клиента')
    number = models.CharField(max_length=22, verbose_name='Телефон номер')
    address = models.CharField(max_length=255, verbose_name='')
    pay = models.PositiveIntegerField(default=0, verbose_name='Тип оплаты',
                                      choices={(0, u'Наличные'), (1, u'Оплата картой')})

    def __str__(self):
        return self.address

    class Meta:
        verbose_name='Закупка'
        verbose_name_plural='Закупки'