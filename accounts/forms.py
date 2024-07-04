from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserAccountModel

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'id':'required'}))
    last_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'id':'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id':'required'}))
    class Meta : 
        model = User
        fields = ['username','first_name','last_name','email']



class DepositeForm(forms.ModelForm):
    class Meta:
        model = UserAccountModel
        fields = ['amount']



class ProfileUpdateForm(forms.ModelForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']