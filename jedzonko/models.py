from django.db import models
from django.utils.text import slugify


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.SmallIntegerField()
    preparation = models.TextField()
    votes = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')

    def __str__(self):
        return self.name


class DayName(models.Model):
    day_name = models.CharField(max_length=16)
    order = models.SmallIntegerField()

    def __str__(self):
        return self.day_name


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=84)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)

    @staticmethod
    def get_recipe_plan_data(plan_id):
        """ structure of recipe_plan_data
        recipe_plan_data = {
            'id': plan_id,
            'name': 'plan name',
            'description': 'plan description',
            'days': [
                {
                    'id': day_id,
                    'name': 'day name',
                    'meals': [
                        {
                            'id': meal_id,
                            'name': 'meal name',
                            'recipe_id': recipe_id,
                            'recipe_name': 'recipe name',
                        },
                        {
                            ...
                        }
                    ]
                },
                {
                    ...
                },
            ]
        }
        """
        recipe_plan = RecipePlan.objects.filter(plan_id=plan_id).order_by('day_name__order', 'order')
        if len(recipe_plan):
            recipe_plan_data = {
                'id': recipe_plan[0].plan.id,
                'name': recipe_plan[0].plan.name,
                'description': recipe_plan[0].plan.description,
                'days': [],
            }
            meals = []
            for i in range(len(recipe_plan)):
                meals.append({
                    'id': recipe_plan[i].id,
                    'name': recipe_plan[i].meal_name,
                    'recipe_id': recipe_plan[i].recipe.id,
                    'recipe_name': recipe_plan[i].recipe.name,
                })
                if i + 1 == len(recipe_plan) or recipe_plan[i + 1].day_name_id != recipe_plan[i].day_name_id:
                    recipe_plan_data['days'].append({
                        'id': recipe_plan[i].day_name.id,
                        'name': recipe_plan[i].day_name.day_name,
                        'meals': meals,
                    })
                    meals = []
        else:
            plan = Plan.objects.get(pk=plan_id)
            recipe_plan_data = {
                'id': plan.id,
                'name': plan.name,
                'description': plan.description,
                'days': [],
            }
        return recipe_plan_data


class Page(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
