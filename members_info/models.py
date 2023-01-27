from django.db import models

# Create your models here.

class members(models.Model):
    roll=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    marks=models.CharField(max_length=255)