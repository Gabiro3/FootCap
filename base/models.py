from django.db import models
from django.contrib.auth.models import AbstractUser

#User Model
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    products = list()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

#Products Model
class Testimonial(models.Model):
    user = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    rating = models.CharField(max_length=50)


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=100)
    category = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)

    def __str__(self):
        return self.name
