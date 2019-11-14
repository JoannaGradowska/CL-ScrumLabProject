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

    @staticmethod
    def get_data(plan_id):
        # recipeplan dict structure
        # recipeplan = {
        #     'name': 'nazwa planu',
        #     'description': 'opis planu',
        #     'days': {
        #         1: {
        #             'day_name': 'nazwa dnia,'
        #             'meals': {
        #                 1: {
        #                     'meal_name': 'nazwa posilku',
        #                     'recipe_id': id_przepisu,
        #                     'recipe_name': 'nazwa przepisu',
        #                 }
        #             }
        #         }
        #     }
        # }
        recipeplan = {'days': {}}
        plan = RecipePlan.objects.filter(plan_id=plan_id)
        for rp in plan:
            recipeplan['name'] = rp.plan.name
            recipeplan['description'] = rp.plan.description
            if rp.day_name_id not in recipeplan['days']:
                recipeplan['days'].update({
                    rp.day_name_id: {
                        'day_name': rp.day_name.day_name,
                        'meals': {},
                    },
                })
            if rp.id not in recipeplan['days'][rp.day_name_id]['meals']:
                recipeplan['days'][rp.day_name_id]['meals'].update({
                    rp.id: {
                        'meal_name': rp.meal_name,
                        'recipe_id': rp.recipe.id,
                        'recipe_name': rp.recipe.name,
                    },
                })
        return recipeplan
