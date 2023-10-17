from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MyValidationForm(forms.Form):

    sc_codigo = forms.IntegerField(required=False)
    sc_nombre = forms.CharField(required=False)
    p_codigo = forms.CharField(required=False)
    p_nombre = forms.CharField(required=False)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
