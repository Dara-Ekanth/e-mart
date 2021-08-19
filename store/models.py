from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
# class Customer(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
#     name=models.CharField(max_length=200,null=True)
#     email=models.CharField(max_length=200,null=True)
#
#     def __str__(self):
#         return self.name

Customer = settings.AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True, default='this is the descriptions')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    complete = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    payment_id = models.CharField(max_length=100, blank=False, default="due payment")
    order_id = models.CharField(max_length=100, blank=False)
    paidto_wallet = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{str(self.customer)} {str(self.order_id)}"

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
