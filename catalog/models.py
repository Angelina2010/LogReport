from __future__ import unicode_literals

from django.contrib import auth
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from pytz import unicode
from transliterate import translit


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    okpo = models.IntegerField()
    phone = models.IntegerField()
    post = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    sign = models.ImageField(upload_to=image_folder)
    is_provider = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


def pre_save_company_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(unicode(instance.full_name), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_company_slug, sender=Company)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(unicode(instance.name), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class ProductManager(models.Manager):

    def all(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().filter(available=True)


class Product(models.Model):
    owner = models.ForeignKey(Company, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})


def pre_save_product_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(unicode(instance.title), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_product_slug, sender=Product)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return "Cart item for product {0}".format(self.product.title)


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __unicode__(self):
        return self.id

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product,
                                                     item_total=product.price)
        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        for ci in cart.items.all():
            if ci.product == product:
                cart.items.remove(ci)
                cart.save()


class Order(models.Model):
    owner = models.ForeignKey(Company, on_delete=models.PROTECT)
    user = models.ForeignKey(auth.get_user_model(), on_delete=models.PROTECT)
    name = models.CharField(max_length=120)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    phone = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True)
    comments = models.TextField()
    slug = models.SlugField(blank=True)
    path = models.CharField(max_length=300, blank=True)
    items = models.ManyToManyField(Cart)

    def __str__(self):
        return "Заказ №{0}".format(str(self.id))

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'order_slug': self.slug})

