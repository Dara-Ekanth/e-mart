from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
#comment for commit
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female')
]


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(unique=True)
    Gender = models.CharField(max_length=6, choices=GENDER_CHOICES,default='Male')
    Birthday = models.DateTimeField(null=True,blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    profile_pic = models.ImageField(default="default.png",null=True, blank=True)
    proof = models.ImageField(default="default_proof.JPG",blank=True,null=True)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=12, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=12, blank=True, null=True)
