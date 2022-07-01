from django.forms import ModelForm, EmailField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


class RegisterForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'image')
