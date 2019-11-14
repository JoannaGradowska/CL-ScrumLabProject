from django import forms
# from django.forms import ModelForm
from jedzonko.models import Recipe, Plan


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'description', 'preparation_time']


class AddPlanForm(forms.Form):
    name = forms.CharField(
        min_length=5,
        max_length=255,
        strip=True,
        label="Nazwa planu",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'nazwa planu'}
        )
    )
    description = forms.CharField(
        min_length=10,
        strip=True,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'opis planu'}
        )
    )
