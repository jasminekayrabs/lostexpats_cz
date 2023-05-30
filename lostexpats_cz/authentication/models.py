from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class MyModel(models.Model):
    fname = models.CharField(max_length=30, default='')
    lname = models.CharField(max_length=30, default='')
    email = models.EmailField()
    date = models.DateField(default=datetime.date.today)


#Defining cookies
class CookieType(models.Model):
    TYPE_CHOICES = [
        ('functional', 'Functional'),
        ('advertising', 'Advertising'),
        ('analytics', 'Analytics'),
        ('essential', 'Essential'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.type

class CookieConsent(models.Model):
    TYPES = ['functional', 'advertising', 'analytics', 'essential']
    session_id = models.CharField(max_length=255, blank=True,  null=True)
    functional = models.BooleanField(null=True, default=False)
    advertising = models.BooleanField(null=True, default=False)
    analytics = models.BooleanField(null=True, default=False)
    essential = models.BooleanField(null=True, default=False)
