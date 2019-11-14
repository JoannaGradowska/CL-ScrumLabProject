from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.SmallIntegerField()
    preparation = models.TextField()
    votes = models.SmallIntegerField(default=0)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')


class DayName(models.Model):
    day_name = models.CharField(max_length=16)
    order = models.SmallIntegerField()


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=84)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)

