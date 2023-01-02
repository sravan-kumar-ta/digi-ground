from django.db import models
from django.utils import timezone

from account.models import CustomUser, Address
from products.models import Product


class Order(models.Model):
    status_choices = (
        (1, 'Order Confirmed'),
        (2, 'Shipped'),
        (3, 'Delivered')
    )
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE'),
        (3, 'PENDING'),
    )

    order_id = models.CharField(unique=True, max_length=50, null=True, blank=True, default=None)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    sub_total = models.FloatField()
    tax = models.FloatField()
    shipping_charge = models.FloatField()
    discount = models.FloatField()
    grand_total = models.FloatField()

    order_status = models.IntegerField(choices=status_choices, default=1)
    payment_status = models.IntegerField(choices=payment_status_choices, default=3)
    datetime_of_payment = models.DateTimeField(default=timezone.now)

    # related to razorpay
    razorpay_order_id = models.CharField(max_length=150, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=150, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=150, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_of_payment and self.pk:
            self.order_id = self.datetime_of_payment.strftime('%y%m%dODR') + str(self.pk)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user) + "|" + str(self.order_id)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = (('order', 'product'),)
