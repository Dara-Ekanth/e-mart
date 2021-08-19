from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

# class (models.Model):
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100, null=True)
#
#     def __str__(self):
#         return str(self.user)


customer = settings.AUTH_USER_MODEL


# class bill(models.Model):
#     name = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True)
#     amount = models.CharField(max_length=25)
#     payment_id = models.CharField(max_length=100, blank=False, default="due payment")
#     order_id = models.CharField(max_length=100, blank=False)
#     email = models.EmailField(max_length=100, null=True)
#     paid = models.BooleanField(default=False)
#
#     def __str__(self):
#         return str(self.order_id)


class wallet(models.Model):
    name = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return str(self.balance)
