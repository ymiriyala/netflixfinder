from django.db import models

class userreg(models.Model):
    username = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

class userlog(models.Model):
    userId = models.IntegerField(11)
    name = models.CharField(max_length=128)

class insertMovie(models.Model):
    name = models.CharField(max_length=128)
    rating = models.CharField(max_length=128)
    userId = models.IntegerField(11)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

class removeMovie(models.Model):
    titleId = models.CharField(max_length=128)
    watchId = models.IntegerField(max_length=11)
    userId = models.IntegerField(11)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

class searchMovie(models.Model):
    name = models.CharField(max_length=128)

class editRating(models.Model):
    titleId = models.CharField(max_length=128)
    userId = models.IntegerField(11)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    rating = models.IntegerField(32)
