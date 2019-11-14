from datetime import datetime

from django.db import DatabaseError
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from jedzonko.models import *
from jedzonko.forms import *


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class LandingPage(View):

    def get(self, request):
        plan = Plan.objects.last()
        print(plan)
        return render(request, "index.html", {
            'plans_counter': Plan.objects.all().count(),
            'recipes_counter': Recipe.objects.all().count(),
            'random_recipes': Recipe.objects.order_by('?')[:3],
            'last_plan': Plan.objects.last(),
        })


class Dashboard(View):

    def get(self, request):
        return render(request, 'dashboard.html', {
            'recipes_counter': Recipe.objects.all().count(),
            'plans_counter': Plan.objects.all().count(),
            'last_plan': Plan.objects.last(),
            'day_name': DayName.objects.first(),
        })


class RecipeDetails(View):

    def get(self, request, id=None):
        return HttpResponse('<a href="javascript:history.back()">back</a>')


class RecipeList(View):

    def get(self, request):
        return render(request, 'app-recipes.html')


class RecipeAdd(View):
    def get(self, request):
        form = AddRecipeForm()
        return render(request, 'app-add-recipe.html', context={'form': form})

    def post(self, request):
        form = AddRecipeForm(request.POST)
        form.save()
        form = AddRecipeForm()
        return render(request, 'app-add-recipe.html', context={'form': form, 'added': "Dodano nowy przepis"})


class RecipeModify(View):

    def get(self, request, id=None):
        return HttpResponse('<a href="javascript:history.back()">back</a>')


class PlanDetails(View):

    def get(self, request, id=None):
        return HttpResponse('<a href="javascript:history.back()">back</a>')


class PlanList(View):

    def get(self, request):
        return HttpResponse('<a href="javascript:history.back()">back</a>')


class PlanAdd(View):

    def get(self, request):
        return HttpResponse('<a href="javascript:history.back()">back</a>')


class PlanAddRecipe(View):
    def get(self, request):
        return render(request, 'app-schedules-meal-recipe.html', {
            'recipes': Recipe.objects.all(),
            'plans': Plan.objects.all(),
            'days': DayName.objects.all(),

        })
    def post(self, request):
        try:
            plan = RecipePlan()
            plan.plan_id = int(request.POST.get('plan_id'))
            plan.meal_name = request.POST.get('meal_name')
            plan.order = int(request.POST.get('order'))
            plan.recipe_id = int(request.POST.get('recipe_id'))
            plan.day_name_id = int(request.POST.get('day_id'))
            plan.save()
            save = True
        except DatabaseError as e:
            print(e)
            saved = False
        return render(request, 'app-schedules-meal-recipe.html', context={'added': 'dodano przepis do planu'})



