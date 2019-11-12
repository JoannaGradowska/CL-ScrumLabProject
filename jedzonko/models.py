from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(datetime.now())
    updated = models.DateTimeField(datetime.now())
    preparation_time = models.SmallIntegerField()
    votes = models.SmallIntegerField(default=0)
