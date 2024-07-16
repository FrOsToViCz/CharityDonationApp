from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(Category)

    FOUNDATION = 'fundacja'
    NGO = 'organizacja pozarządowa'
    LOCAL_COLLECTION = 'zbiórka lokalna'
    TYPE_CHOICES = [
        (FOUNDATION, 'fundacja'),
        (NGO, 'organizacja pozarządowa'),
        (LOCAL_COLLECTION, 'zbiórka lokalna'),
    ]

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.quantity} dla {self.institution.name}'
