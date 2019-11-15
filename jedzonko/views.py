from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from jedzonko.models import Plan, Recipe, RecipePlan, DayName
from jedzonko.forms import AddRecipeForm, AddPlanForm, PlanAddRecipeForm


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
            'recipes_counter': Recipe.objects.count(),
            'plans_counter': Plan.objects.count(),
            'plan': RecipePlan.get_recipe_plan_data(plan.plan_id),
        })


class RecipeDetails(View):

    def get(self, request, id=None):
        recipe = Recipe.objects.get(id=id)
        return render(request, 'app-recipe-details.html', context={
            'recipe': recipe,
        })

    def post(self, request, id):
        if request.POST.get('recipe_id') is not None:
            recipe = get_object_or_404(Recipe, pk=int(request.POST.get('recipe_id')))
            if request.POST.get('add') is not None:
                recipe.votes += 1
            elif recipe.votes > 0:
                recipe.votes -= 1
            recipe.save()
            return redirect(f"/recipe/{request.POST.get('recipe_id')}/")
        return redirect(request.META['PATH_INFO'])


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
            'plan': RecipePlan.get_recipe_plan_data(id)
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
            'form': PlanAddRecipeForm(),
        })

    def post(self, request):
        form = PlanAddRecipeForm(request.POST)
        if form.is_valid():
            plan = RecipePlan()
            plan.meal_name = form.cleaned_data['meal_name']
            plan.order = form.cleaned_data['order']
            plan.day_name = form.cleaned_data['day_name_id']
            plan.plan = form.cleaned_data['plan_id']
            plan.recipe = form.cleaned_data['recipe_id']
            plan.save()
            return redirect(f"/plan/{plan.plan_id}/")
        else:
            return render(request, 'app-schedules-meal-recipe.html', {
                'form': form,
            })
