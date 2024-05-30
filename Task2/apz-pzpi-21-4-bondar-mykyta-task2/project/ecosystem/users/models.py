from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    payment_key = models.CharField(max_length=100, null=True, blank=True)
    all_payment_keys = ArrayField(models.CharField(max_length=100), null=True, blank=True)


    def __str__(self):
        return self.username
