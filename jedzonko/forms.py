from django import forms
from jedzonko.models import Recipe, Plan, DayName


class AddModifyRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'description', 'preparation_time', 'preparation']
        labels = {
            'name': 'Nazwa przepisu',
            'ingredients': 'Składniki',
            'description': 'Opis przepisu',
            'preparation_time': 'Czas przygotowania',
            'preparation': 'Sposób przygotowania',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-100 p-1', 'placeholder': 'nazwa przepisu'}),
            'description': forms.Textarea(attrs={'class': 'w-100 p-1', 'rows': 5, 'placeholder': 'opis przepisu'}),
            'preparation_time': forms.NumberInput(attrs={'class': 'p-1', 'placeholder': 'minuty', 'min': 1}),
            'preparation': forms.Textarea(attrs={'class': 'w-100 p-1', 'rows': 10, 'placeholder': 'sposób przygotowania'}),
            'ingredients': forms.Textarea(attrs={'class': 'w-100 p-1', 'rows': 10, 'placeholder': 'potrzebne składniki'}),
        }


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


class PlanAddRecipeForm(forms.Form):
    plan_id = forms.ModelChoiceField(
        queryset=Plan.objects.all().order_by('name'),
        label='Wybierz plan',
        widget=forms.Select(
            attrs={'class': 'custom-select mb-3 autowidth'},
        ),
    )
    meal_name = forms.CharField(
        min_length=3,
        max_length=84,
        strip=True,
        label='Nazwa posiłku',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'nazwa posiłku'},
        ),
    )
    order = forms.IntegerField(
        min_value=1,
        label='Numer posiłku',
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'pozycja na liście'},
        ),
    )
    recipe_id = forms.ModelChoiceField(
        queryset=Recipe.objects.all().order_by('name'),
        label='Przepis',
        widget=forms.Select(
            attrs={'class': 'form-control'},
        ),
    )
    day_name_id = forms.ModelChoiceField(
        queryset=DayName.objects.all().order_by('order'),
        label='Dzień',
        widget=forms.Select(
            attrs={'class': 'form-control'},
        ),
    )
