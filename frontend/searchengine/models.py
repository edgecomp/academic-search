from django.db import models


# Create your models here.
class Conferences(models.Model):
    conference_name = models.TextField(primary_key=True)
    corpus = models.TextField()
    similar_conference = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conferences'


class Keywords(models.Model):
    id = models.IntegerField(primary_key=True)
    keyword = models.TextField()
    score = models.FloatField()
    conference_name = models.ForeignKey(Conferences, models.DO_NOTHING, db_column='conference_name', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keywords'


class Metadata(models.Model):
    id = models.IntegerField(primary_key=True)
    conference_type = models.TextField()
    year = models.IntegerField()
    title = models.TextField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    conference_name = models.ForeignKey(Conferences, models.DO_NOTHING, db_column='conference_name', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metadata'
