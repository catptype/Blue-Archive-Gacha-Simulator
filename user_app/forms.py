import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Achievement

class CreateNewUserForm(UserCreationForm):

    def clean_username(self):
        username = self.cleaned_data['username']
        
        if not re.match(r'^[a-zA-Z0-9@.+\-_]+$', username):
            raise ValidationError('Username contain only letters, numbers, and @/./+/-/_ characters.')

        return username
    
    username = forms.CharField(
        max_length=20,
        label='Username',
        widget=forms.TextInput(attrs={'size':'24', 'class':'inputText'}), # For controling, width size
        help_text='Enter a username with a maximum of 20 characters long.',
        error_messages={
            'unique': 'This username is already taken.',
        },
    )

    password1 = forms.CharField(
        min_length=8,
        max_length=20,
        label='Password',
        widget=forms.PasswordInput(render_value=True, attrs={'size':'24', 'class':'inputText'}), # For controling, width size
        help_text='Your password must be between 8 and 20 characters long.',
    )

    password2 = forms.CharField(
        min_length=8,
        max_length=20,
        label='Confirm Password',
        widget=forms.PasswordInput(render_value=True, attrs={'size':'24', 'class':'inputText'}), # For controling, width size
        help_text='Enter the same password as before, for verification.',
        error_messages={
            "password_too_common": "This password is too common.",
            "password_entirely_numeric": "This password is entirely numeric.",
            "password_mismatch": "The two password fields didn't match.",
        },
    )
    
    tos = forms.BooleanField(
        required=True,
        label="I accept the Terms of Service",
        error_messages={
            'required': 'You must accept the Terms of Service to proceed.'
        }
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'tos']

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override attibutes for form elements
        self.fields['username'].widget.attrs['size'] = 24
        self.fields['username'].widget.attrs['maxlength'] = 20
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

        self.fields['password'].widget.attrs['size'] = 24
        self.fields['password'].widget.attrs['maxlength'] = 20
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

    username = forms.CharField(
        max_length=20,
        label='Username',
        widget=forms.TextInput(), # For controling, width size
    )

    password = forms.CharField(
        max_length=20,
        label='Password',
        widget=forms.PasswordInput(), # For controling, width size
    )

    error_messages = {
        'invalid_login': "Invalid username or password."
    }

class AchievementAdminForm(forms.ModelForm):

    image = forms.ImageField(
        label="Achievement icon",
        widget=forms.ClearableFileInput(), 
        required=False,
    )

    class Meta:
        model = Achievement
        fields = '__all__'
        widgets = {
            'criteria': FilteredSelectMultiple('Criteria', is_stacked=False),
        }