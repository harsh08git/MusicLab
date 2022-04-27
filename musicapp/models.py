from django.db import models

# Create your models here.



class Genres(models.Model):
    track_name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    popularity = models.IntegerField()


class Mood(models.Model):
    track_name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    mood = models.CharField(max_length=200)

