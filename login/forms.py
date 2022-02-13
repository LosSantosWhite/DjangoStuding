from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Имя')
    last_name = forms.CharField(max_length=30, required=True, help_text='Фамилия')
    date_of_birth = forms.DateField(required=False, help_text='Дата рождения')
    city = forms.CharField(max_length=30, required=False, help_text='Город')
    phone_number = forms.CharField(max_length=11, required=False, help_text='Номер телефона для верификации')
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',]

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'city', 'phone_number']