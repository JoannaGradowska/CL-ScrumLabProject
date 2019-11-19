"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from jedzonko import views

urlpatterns = [
    path('', views.LandingPage.as_view()),
    path('admin/', admin.site.urls),
    path('main/', views.Dashboard.as_view()),

    path('recipe/<int:id>/', views.RecipeDetails.as_view()),
    path('recipe/list/', views.RecipeList.as_view()),
    path('recipe/list/<int:page>/', views.RecipeList.as_view()),
    path('recipe/add/', views.RecipeAdd.as_view()),
    path('recipe/modify/<int:id>/', views.RecipeModify.as_view()),
    path('recipe/delete/<int:recipe_id>/', views.DeleteRecipe.as_view()),

    path('plan/<int:id>/', views.PlanDetails.as_view()),
    path('plan/list/', views.PlanList.as_view()),
    path('plan/list/<int:page>/', views.PlanList.as_view()),
    path('plan/add/', views.PlanAdd.as_view()),
    path('plan/add-recipe/', views.PlanAddRecipe.as_view(), name='process'),
    path('plan/delete-meal/<int:meal_id>/', views.PlanDeleteMeal.as_view()),
    path('plan/modify/<int:plan_id>/', views.PlanModify.as_view()),

    path('<slug>/', views.ViewPage.as_view()),
]
