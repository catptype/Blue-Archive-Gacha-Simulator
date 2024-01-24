import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple


from .models import Achievement

class CreateNewUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override attibutes for form elements
        self.fields['username'].widget.attrs['maxlength'] = 20
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['first_name'].widget.attrs['maxlength'] = 20
        self.fields['first_name'].widget.attrs['placeholder'] = 'Display name'
        self.fields['password1'].widget.attrs['maxlength'] = 20
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['maxlength'] = 20
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username', '')
        first_name = cleaned_data.get('first_name', '')

        if not re.match(r'^[a-zA-Z0-9.@+-_]*$', username):
            self.add_error('username', ValidationError("Only letters, numbers, and '@.+-_' are allowed."))

        if not re.match(r'^[a-zA-Z0-9]*$', first_name):
            self.add_error('name', ValidationError('Only letters and numbers are allowed.'))
        
    username = forms.CharField(
        max_length=20,
        label='Username',
        widget=forms.TextInput(),
        help_text='Enter a username with a maximum of 20 characters long.',
        error_messages={
            'unique': 'This username is already taken.',
            'required': 'This field is required.',
        },
    )

    first_name = forms.CharField(
        max_length=20,
        label='Display name',
        widget=forms.TextInput(),
        help_text='Enter a display name with a maximum of 20 characters long.',
        error_messages={
            'required': 'This field is required.',
        },
    )

    password1 = forms.CharField(
        min_length=8,
        max_length=20,
        label='Password',
        widget=forms.PasswordInput(render_value=True),
        help_text='Your password must be between 8 and 20 characters long.',
        error_messages={
            'required': 'This field is required.',
            "password_too_common": "This password is too common.",
            "password_entirely_numeric": "This password is entirely numeric.",
        }
    )

    password2 = forms.CharField(
        min_length=8,
        max_length=20,
        label='Confirm Password',
        widget=forms.PasswordInput(render_value=True),
        help_text='Enter the same password as before, for verification.',
        error_messages={
            "password_mismatch": "The two password fields do not match.",
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
        fields = ['username', 'first_name', 'password1', 'password2', 'tos']

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override attibutes for form elements
        self.fields['username'].widget.attrs['maxlength'] = 20
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['maxlength'] = 20
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

    username = forms.CharField(
        max_length=20,
        label='Username',
        widget=forms.TextInput(), # For controling, width size
        error_messages={
            'required': 'This field is required.',
        },
    )

    password = forms.CharField(
        max_length=20,
        label='Password',
        widget=forms.PasswordInput(), # For controling, width size
        error_messages={
            'required': 'This field is required.',
        },
    )

    error_messages = {
        'invalid_login': "Invalid username or password."
    }

class ForgotPasswordForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override attibutes for form elements
        self.fields['username'].widget.attrs['maxlength'] = 20
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['first_name'].widget.attrs['maxlength'] = 20
        self.fields['first_name'].widget.attrs['placeholder'] = 'Display name'
        self.fields['password1'].widget.attrs['maxlength'] = 20
        self.fields['password1'].widget.attrs['placeholder'] = 'New password'
        self.fields['password2'].widget.attrs['maxlength'] = 20
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm new password'

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username', None)
        first_name = cleaned_data.get('first_name', None)
        password1 = cleaned_data.get('password1', None)
        password2 = cleaned_data.get('password2', None)

        try:
            user_instance = User.objects.get(username=username, first_name=first_name)
            old_password = user_instance.password
            if check_password(password1, old_password) and password1 and password2:
                raise ValidationError('New password exactly same as old password')
            
            # Validate the new password against AUTH_PASSWORD_VALIDATORS
            validate_password(password1, user_instance)

            # Check if the new passwords match
            if password1 != password2 and password1 and password2:
                self.add_error('password1', 'Password do not match.')
                self.add_error('password2', 'Password do not match.')

        except User.DoesNotExist:
            if username and first_name:
                raise ValidationError('Username and Display name not match.')

        return cleaned_data
    
    username = forms.CharField(
        max_length=20,
        label='Username',
        widget=forms.TextInput(), # For controling, width size
        error_messages={
            'required': 'This field is required.',
        },
    )

    first_name = forms.CharField(
        max_length=20,
        label='Display name',
        widget=forms.TextInput(), # For controling, width size
        error_messages={
            'required': 'This field is required.',
        },
    )

    password1 = forms.CharField(
        min_length=8,
        max_length=20,
        label='New password',
        widget=forms.PasswordInput(render_value=True),
        help_text='Your password must be between 8 and 20 characters long.',
        error_messages={
            'required': 'This field is required.',
            "password_too_common": "This password is too common.",
            "password_entirely_numeric": "This password is entirely numeric.",
        }
    )

    password2 = forms.CharField(
        min_length=8,
        max_length=20,
        label='Confirm new password',
        widget=forms.PasswordInput(render_value=True),
        help_text='Enter the same password as before, for verification.',
        error_messages={
            "password_mismatch": "The two password fields do not match.",
        },
    )

    
    
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