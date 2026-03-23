from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


_CTRL = "form-control bg-dark text-light border-secondary"


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Optional.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("username", "email", "password1", "password2"):
            self.fields[name].widget.attrs.setdefault("class", _CTRL)
