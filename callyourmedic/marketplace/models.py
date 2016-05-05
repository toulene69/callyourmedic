from django.db import models

# Create your models here.

class Marketplace(models.Model):

    apikey =  models.CharField(max_length=17,unique = True)