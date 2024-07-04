from .models import CategoryModel
from django import forms

class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = '__all__'