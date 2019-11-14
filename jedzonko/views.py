from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from jedzonko.models import Plan, Recipe
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
        return render(request, 'dashboard.html')


class RecipeDetails(View):

    def get(self, request, id=None):
        return HttpResponse('<a href="javascript:history.back()">back</a>')


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
        return HttpResponse('<a href="javascript:history.back()">back</a>')


class PlanList(View):

    def get(self, request, page=1):
        plans = Plan.objects.all().extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
        paginator = Paginator(plans, 2) # na czas testow, docelowo 50
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
        return HttpResponse('<a href="javascript:history.back()">back</a>')

