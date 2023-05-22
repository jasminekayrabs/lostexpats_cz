from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class MyModel(models.Model):
    fname = models.CharField(max_length=30, default='')
    lname = models.CharField(max_length=30, default='')
    email = models.EmailField()
    date = models.DateField(default=datetime.date.today)



