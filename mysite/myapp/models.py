from django.db import models

class Person(models.Model):
    username = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
