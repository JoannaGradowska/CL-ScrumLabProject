from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q
from jedzonko.models import Plan, Recipe, RecipePlan, Page
from jedzonko.forms import AddModifyRecipeForm, AddPlanForm, PlanAddRecipeForm
from .settings import *
import re


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

    def get(self, request, id):
        return render(request, 'app-recipe-details.html', context={
            'recipe': Recipe.objects.get(id=id),
            'back_link': '/recipe/list/' if request.GET.get('ref') is None else request.GET.get('ref'),
        })

    def post(self, request, id):
        if request.POST.get('recipe_id') is not None:
            recipe = get_object_or_404(Recipe, pk=int(request.POST.get('recipe_id')))
            if request.POST.get('add') is not None:
                recipe.votes += 1
            elif recipe.votes > 0:
                recipe.votes -= 1
            recipe.save()
            ref = f'/recipe/list/1/' if request.GET.get('ref') is None else request.GET.get('ref')
            return redirect(f"/recipe/{request.POST.get('recipe_id')}/?ref={ref}")
        return redirect(request.META['PATH_INFO'])


class RecipeList(View):

    def get(self, request, page=1):
        q = Q()
        if request.GET.get('search') is not None:
            q |= Q(name__icontains=request.GET.get('search'))
            q |= Q(description__icontains=request.GET.get('search'))
        recipes = Recipe.objects.filter(q).order_by('-votes', '-created')
        recipes = Paginator(recipes, PAGIN_RECIPES_PER_PAGE)
        recipes = recipes.get_page(page)
        if request.GET.get('search') is not None:
            for recipe in recipes:
                recipe.name = re.sub(rf"({request.GET.get('search')})", r'<b>\1</b>', recipe.name, flags=re.I)
                recipe.description = re.sub(rf"({request.GET.get('search')})", r'<b>\1</b>', recipe.description, flags=re.I)
        return render(request, 'app-recipes.html', {
            'recipes': recipes,
        })


class RecipeAdd(View):

    def get(self, request):
        form = AddModifyRecipeForm()
        return render(request, 'app-add-recipe.html', context={'form': form})

    def post(self, request):
        form = AddModifyRecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/recipe/list/')
        return render(request, 'app-add-recipe.html', context={
            'form': form,
            'error_message': "Wypełnij poprawnie wszystkie pola",
        })


class RecipeModify(View):

    def get(self, request, id=None):
        recipe = get_object_or_404(Recipe, pk=id)
        form = AddModifyRecipeForm(instance=recipe)
        return render(request, 'app-edit-recipe.html', context={
            'form': form,
            'recipe_id': recipe.id,
        })

    def post(self, request, id=None):
        # ponizszej linii uzyjemy, jak bedziemy chcieli edytowac ten sam przepis
        # form = ModifyRecipeForm(request.POST, instance=Recipe.objects.get(pk=id))
        form = AddModifyRecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/recipe/list/')
        return redirect(f"/recipe/modify/{request.POST.get('recipe_id')}/?error")


class PlanDetails(View):

    def get(self, request, id=None):
        return render(request, 'app-details-schedules.html', context={
            'plan': RecipePlan.get_recipe_plan_data(id),
            'back_link': '/plan/list/' if request.GET.get('ref') is None else request.GET.get('ref'),
        })


class PlanList(View):

    def get(self, request, page=1):
        plans = Plan.objects.all().extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
        paginator = Paginator(plans, PAGIN_PLANS_PER_PAGE)
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


class PlanDeleteMeal(View):

    def get(self, request, meal_id):
        return render(request, 'app-plan-delete-meal.html', context={
            'meal': get_object_or_404(RecipePlan, pk=meal_id),
        })

    def post(self, request, meal_id):
        if meal_id == int(request.POST.get('meal_id')):
            meal = get_object_or_404(RecipePlan, pk=meal_id)
            meal.delete()
            return redirect(f'/plan/{meal.plan_id}/')
        return self.get(request, meal_id)


class ViewPage(View):

    def get(self, request, slug):
        return render(request, 'page.html', context={
            'page': get_object_or_404(Page, slug=slug)
        })
