# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Conferences(models.Model):
    conference_name = models.TextField(primary_key=True)
    corpus = models.TextField()
    similar_conference = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conferences'


class ConferencesTemp(models.Model):
    conference_name = models.TextField(primary_key=True)
    corpus = models.TextField()
    similar_conference = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conferences_temp'


class Keywords(models.Model):
    keyword = models.TextField()
    score = models.FloatField()
    conference_name = models.ForeignKey(Conferences, models.DO_NOTHING, db_column='conference_name', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keywords'


class KeywordsTemp(models.Model):
    keyword = models.TextField()
    score = models.FloatField()
    conference_name = models.ForeignKey(ConferencesTemp, models.DO_NOTHING, db_column='conference_name', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keywords_temp'


class Metadata(models.Model):
    conference_type = models.TextField()
    year = models.IntegerField()
    title = models.TextField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    conference_name = models.ForeignKey(Conferences, models.DO_NOTHING, db_column='conference_name', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metadata'


class MetadataTemp(models.Model):
    conference_type = models.TextField()
    year = models.IntegerField()
    title = models.TextField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    conference_name = models.ForeignKey(ConferencesTemp, models.DO_NOTHING, db_column='conference_name', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metadata_temp'


class MetadataTest(models.Model):
    conference_type = models.TextField()
    year = models.IntegerField()
    title = models.TextField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    conference_name = models.ForeignKey(ConferencesTemp, models.DO_NOTHING, db_column='conference_name', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metadata_test'
