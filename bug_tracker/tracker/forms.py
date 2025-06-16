from django import forms
from django.contrib.auth.models import User
from .models import Bug, Project
from django.contrib.auth.forms import UserCreationForm

class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['changeset_id', 'title', 'description', 'status', 'assigned_to', 'project']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

class BugUpdateForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['title', 'description', 'status', 'assigned_to', 'project', 'changeset_id']