from django.db import models

class userreg(models.Model):
    username = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

class userlog(models.Model):
    userId = models.IntegerField(11)
    name = models.CharField(max_length=128)
