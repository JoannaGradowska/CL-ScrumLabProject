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
    path('', views.LocalPage.as_view()),
    path('admin/', admin.site.urls),
    path('index/', views.IndexView.as_view()),
    path('main/', views.Dashboard.as_view()),
    path('recipe/<id>/', views.RecipeDetails.as_view()),
    path('recipe/list/', views.RecipeList.as_view()),
    path('recipe/add/', views.RecipeAdd.as_view()),
    path('recipe/modify/<id>/', views.RecipeModify.as_view()),
    path('plan/<id>/', views.PlanDetails.as_view()),
    path('plan/add/', views.PlanAdd.as_view()),
    path('plan/add-recipe/', views.PlanAddRecipe.as_view()),
]
