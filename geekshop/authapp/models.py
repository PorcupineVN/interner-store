from django.db import models
from django.contrib.auth.models import AbstractUser



class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(verbose_name='Возраст')
    avatar = models.ImageField(verbose_name='Аватарка', blank=True, upload_to='users')
    phone = models.CharField(verbose_name='Телефон', max_length=10, blank=True)
    city = models.CharField(verbose_name='Город', max_length=20, blank=True)
