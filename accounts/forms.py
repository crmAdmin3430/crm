from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ManagerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Для всех полей убираем help_text
        for field in self.fields.values():
            field.help_text = ""