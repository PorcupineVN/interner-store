from pyexpat import model
from tabnanny import verbose
from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=100)
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.name

class ProductManager(models.Manager):

    def active_items(self):
        return Product.objects.filter(is_active=True)

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField (verbose_name='имя', max_length=100)
    price = models.DecimalField(verbose_name='цена', max_digits=7, decimal_places=2, default=0, db_index=True)
    color = models.PositiveIntegerField(verbose_name='цвет', default=0x000000)
    description = models.TextField(verbose_name='описание', blank=True)
    image = models.ImageField(verbose_name='картинка', blank=True, upload_to='products')
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0, db_index=True)
    is_active = models.BooleanField(verbose_name='активный', default=True, db_index=True)

    objects = ProductManager()

    def __str__(self):
        return self.name
   