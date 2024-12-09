from django import forms
from .models import Image
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['original_image']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    error_messages = {
        'password_mismatch': 'The two password fields didn’t match.',
        'password_too_similar': 'Your password is too similar to your personal information.',
        'password_too_short': 'Your password must contain at least 8 characters.',
        'password_too_common': 'Your password is too common.',
        'password_entirely_numeric': 'Your password can’t be entirely numeric.',
    }
from django import forms
from django.contrib.auth.models import User

class SendImageForm(forms.Form):
    recipient_username = forms.CharField(max_length=150, help_text="Enter the username of the recipient")

