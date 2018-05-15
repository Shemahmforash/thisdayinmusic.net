from django.db import models


class User(models.Model):
    username = models.CharField(max_length=60, unique=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Playlist(models.Model):
    spotify_id = models.CharField(max_length=60, unique=True)
    date = models.DateField()

    track_ids = models.TextField()
    url = models.CharField(max_length=200)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
