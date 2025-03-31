from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email') # Add other fields as needed

class CustomAuthenticationForm(AuthenticationForm):
    pass # Inherits default behavior, can be customized later if needed
