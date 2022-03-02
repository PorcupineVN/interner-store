from django.db import models
from django.conf import settings
from mainapp.models import Product
from basketapp.models import Basket


class Order(models.Model):
    CREATED = 'CREATED'
    IN_PROCESSING = 'IN_PROCESSING'
    AWAITING_PAYMENT = 'AWAITING_PAYMENT'
    PAID = 'PAID'
    READY = 'READY'
    CANCEL = 'CANCEL'
    FINISHED = 'FINISHED'

    ORDER_STATUS_CHOICES = (
        (CREATED, 'создан'),
        (IN_PROCESSING, 'в обработке'),
        (AWAITING_PAYMENT, 'ожидает оплаты'),
        (PAID, 'оплачен'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
        (FINISHED, 'завершен'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус', 
                              max_length=10,
                              choices=ORDER_STATUS_CHOICES,
                              default='CREATED' )
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    # переопределяем метод, удаляющий объект
    def delete(self):
        for item in self.items.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, 
                              related_name="items",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, 
                                verbose_name='продукт',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество',
                                           default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

