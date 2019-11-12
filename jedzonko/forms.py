from django.forms import ModelForm
from jedzonko.models import Recipe


class AddRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'description', 'preparation_time']
