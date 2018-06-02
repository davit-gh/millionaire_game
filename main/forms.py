from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    """Custom Sign up form."""

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password1', 'password2', )

    def clean(self):
        """
        Valdate that first and last name combination is unique.

        Raise validation error if duplicate is found.
        """
        data = self.cleaned_data
        uname = "{}_{}".format(data['first_name'], data['last_name'])
        dup_user = User.objects.filter(username=uname)
        if dup_user:
            raise forms.ValidationError(
                "User with the same First Name, Last Name already exists."
            )
        return data


class LoginForm(AuthenticationForm):
    """Custom login form."""

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(widget=forms.HiddenInput(), required=False)
    field_order = ('first_name', 'last_name', 'password')

    class Meta:
        fields = ('first_name', 'last_name', 'password', 'username')

    def clean(self):
        """Set username before calling parent's clean method."""
        data = self.cleaned_data
        first_name = data['first_name']
        last_name = data['last_name']
        username = "{}_{}".format(first_name, last_name)
        self.cleaned_data = self.cleaned_data.copy()
        self.cleaned_data['username'] = username
        super(LoginForm, self).clean()
