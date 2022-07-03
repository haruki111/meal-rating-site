from django.forms import ModelForm, TextInput
from .models import MealRating


class DetailForm(ModelForm):
    class Meta:
        model = MealRating
        fields = ['rating']
        widgets = {
            "rating": TextInput(attrs={
                "type": "range",
                "max": 5,
                "min": 0,
                "step": 0.1
            })
        }
