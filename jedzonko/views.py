from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class LocalPage(View):

    def get(self, request):
        return render(request, 'index.html')


class Dashboard(View):

    def get(self, request):
        return render(request, 'dashboard.html')


class RecipeDetails(View):

    def get(self, request, id=None):
        return HttpResponse('<a href="javascript:history.back()">back</a>')


class RecipeList(View):

    def get(self, request):
        return render(request, 'app-recipes.html')


class RecipeAdd(View):

    def get(self, request):
        return HttpResponse('<a href="javascript:history.back()">back</a>')


class RecipeModify(View):

    def get(self, request, id=None):
        return HttpResponse('<a href="javascript:history.back()">back</a>')


class PlanDetails(View):

    def get(self, request, id=None):
        return HttpResponse('<a href="javascript:history.back()">back</a>')


class PlanAdd(View):

    def get(self, request):
        return HttpResponse('<a href="javascript:history.back()">back</a>')


class PlanAddRecipe(View):

    def get(self, request):
        return HttpResponse('<a href="javascript:history.back()">back</a>')
