from django.db import DatabaseError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from jedzonko.models import Plan, Recipe, RecipePlan, DayName
from jedzonko.forms import AddRecipeForm, AddPlanForm


class LandingPage(View):

    def get(self, request):
        return render(request, "index.html", {
            'plans_counter': Plan.objects.all().count(),
            'recipes_counter': Recipe.objects.all().count(),
            'random_recipes': Recipe.objects.order_by('?')[:3],
        })


class Dashboard(View):

    def get(self, request):
        plan = RecipePlan.objects.order_by('-plan_id')[0]
        return render(request, 'dashboard.html', context={
            'plan': RecipePlan.get_data(plan.plan_id)
        })


class RecipeDetails(View):
    def get(self, request, id=None):
        recipes = Recipe.objects.get(id=id)
        return render(request, 'app-recipe-details.html', context={'id': id, 'recipes': recipes})


class RecipeList(View):

    def get(self, request, page=1):
        recipes = Recipe.objects.all().order_by('-votes', '-created')
        paginator = Paginator(recipes, 5)
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {
            'recipes': recipes,
        })


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
        return render(request, 'app-details-schedules.html', context={
            'plan': RecipePlan.get_data(id)
        })


class PlanList(View):

    def get(self, request, page=1):
        plans = Plan.objects.all().extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
        paginator = Paginator(plans, 2)  # na czas testow, docelowo 50
        plans = paginator.get_page(page)
        return render(request, 'app-schedules.html', {
            'plans': plans,
        })


class PlanAdd(View):

    def get(self, request):
        form = AddPlanForm()
        return render(request, 'app-add-schedules.html', context={
            'form': form,
        })

    def post(self, request):
        form = AddPlanForm(request.POST)
        if form.is_valid():
            plan = Plan()
            plan.name = form.cleaned_data['name']
            plan.description = form.cleaned_data['description']
            plan.save()
            return redirect(f'/plan/{plan.id}/')
        else:
            return render(request, 'app-add-schedules.html', context={
                'form': form,
            })


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


