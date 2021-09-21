from django.db import models
import json
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'pk': obj.pk})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class Media(models.Model):

    image = models.ImageField(verbose_name='Изображение')
    work = models.ForeignKey('Work', verbose_name='Проект', on_delete=models.CASCADE, related_name='related_media')

    def __str__(self):
        return str(self.image.url)


class Service(models.Model):

    name = models.CharField(max_length=255, verbose_name='Название услуги')
    works = models.ManyToManyField('Work', blank=True, related_name='related_service', verbose_name='Работы')

    def __str__(self):
        return self.name


class Brand(models.Model):

    name = models.CharField(max_length=255, verbose_name='Марка')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'pk': self.pk})

    @property
    def products(self):
        return json.dumps(Work.objects.filter(brand=self).values())

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'


class Work(models.Model):

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    subtitle = models.CharField(max_length=255, blank=True, verbose_name='Подзаголовок')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, verbose_name='Марка автомобиля')
    description = models.TextField(verbose_name='Описание', null=True)
    services = models.ManyToManyField(Service, blank=True, related_name='related_work', verbose_name='Услуги')

    def __str__(self):
        return self.title

    @property
    def media_for_main_page(self):
        if not Media.objects.filter(work=self):
            return
        return Media.objects.filter(work=self).first().image.url

    @property
    def media_for_detail(self):
        if not Media.objects.filter(work=self):
            return
        return Media.objects.filter(work=self)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})

    @property
    def products(self):
        return json.dumps(Product.objects.filter(category=self).values())

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Имя подкатегории')
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, verbose_name='Подкатегория', blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', blank=True)
    characteristics = models.TextField(verbose_name='Характеристики', blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    recommended_products = models.ManyToManyField('self', blank=True, related_name='related_product_for_recommendations', verbose_name='Рекомендованные продукты')
    works = models.ManyToManyField(Work, blank=True, related_name='related_product', verbose_name='Примеры установки')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество товара')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт {} (для корзины)".format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Customer(models.Model):

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE, default=True)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    city = models.CharField(max_length=255, verbose_name='Город', null=True, blank=True)
    index = models.CharField(max_length=255, verbose_name='Индекс', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_customer', blank=True)

    def __str__(self):
        if not (self.user.first_name and self.user.last_name):
            return self.user.username
        return "Покупатель {} {}".format(self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_PAYED = 'payed'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    PAYING_TYPE_CASH = 'cash'
    PAYING_TYPE_CARD = 'card'
    PAYING_TYPE_ONLINE = 'online'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_PAYED, 'Заказ оплачен'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    DELIVERY_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    PAYING_TYPE_CHOICES = (
        (PAYING_TYPE_CASH, 'Наличными'),
        (PAYING_TYPE_CARD, 'Картой'),
        (PAYING_TYPE_ONLINE, 'Онлайн'),
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    city = models.CharField(max_length=55, verbose_name='Город', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=DELIVERY_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    paying_type = models.CharField(
        max_length=100,
        verbose_name='Способ оплаты',
        choices=PAYING_TYPE_CHOICES,
        default=PAYING_TYPE_CASH
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
