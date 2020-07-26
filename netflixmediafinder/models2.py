# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Imdbratings(models.Model):
    titleid = models.CharField(db_column='titleId', primary_key=True, max_length=128)  # Field name made lowercase.
    avgrating = models.IntegerField(db_column='avgRating', blank=True, null=True)  # Field name made lowercase.
    numvotes = models.IntegerField(db_column='numVotes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'imdbratings'


class Imdbtitles(models.Model):
    titleid = models.CharField(db_column='titleId', primary_key=True, max_length=128)  # Field name made lowercase.
    titletype = models.CharField(db_column='titleType', max_length=128, blank=True, null=True)  # Field name made lowercase.
    primarytitle = models.CharField(db_column='primaryTitle', max_length=128)  # Field name made lowercase.
    originaltitle = models.CharField(db_column='originalTitle', max_length=128, blank=True, null=True)  # Field name made lowercase.
    isadult = models.IntegerField(db_column='isAdult', blank=True, null=True)  # Field name made lowercase.
    startyear = models.IntegerField(db_column='startYear', blank=True, null=True)  # Field name made lowercase.
    endyear = models.IntegerField(db_column='endYear', blank=True, null=True)  # Field name made lowercase.
    runtimeminutes = models.IntegerField(db_column='runtimeMinutes', blank=True, null=True)  # Field name made lowercase.
    genres = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imdbtitles'


class Netflixtitles(models.Model):
    show_id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=128, blank=True, null=True)
    director = models.CharField(max_length=500, blank=True, null=True)
    cast = models.CharField(max_length=3000, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    date_added = models.CharField(max_length=32, blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    rating = models.CharField(max_length=30, blank=True, null=True)
    duration = models.CharField(max_length=30, blank=True, null=True)
    listed_in = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=3000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'netflixtitles'


class Users(models.Model):
    userid = models.AutoField(db_column='userId', primary_key=True)  # Field name made lowercase.
    username = models.CharField(max_length=128)
    passwordhash = models.CharField(db_column='passwordHash', max_length=128)  # Field name made lowercase.
    name = models.CharField(max_length=128)
    personality = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'users'


class Watchedmovies(models.Model):
    watchid = models.AutoField(db_column='watchId', primary_key=True)  # Field name made lowercase.
    titleid = models.ForeignKey(Imdbtitles, models.DO_NOTHING, db_column='titleId')  # Field name made lowercase.
    userid = models.ForeignKey(Users, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    rating = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'watchedmovies'
