from django.forms import ModelForm

from jedzonko.models import Recipe


class AddRecipeView(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'description', 'preparation_time']
