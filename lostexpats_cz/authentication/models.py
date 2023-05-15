from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MyModel(models.Model):
    fname = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name
