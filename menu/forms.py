from django import forms
from django import forms

#MODELS
from .models import (
    Category
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']
        
    def clean_category_name(self):
        return self.cleaned_data['category_name'].capitalize()    