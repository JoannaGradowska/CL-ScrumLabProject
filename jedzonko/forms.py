from django.forms import ModelForm
from jedzonko.models import Recipe, Plan


class AddRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'description', 'preparation_time']


class AddPlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'description']
        labels = {
            'name': 'Nazwa planu',
            'description': 'Opis planu',
        }
