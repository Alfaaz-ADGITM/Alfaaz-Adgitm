from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Member


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        help_texts = {
            'username': 'same as your enrollment roll no.',
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'enrollment_number',
            'student_name',
            'role',
            'phone_number',
            'gender',
            'course',
            'branch',]

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)