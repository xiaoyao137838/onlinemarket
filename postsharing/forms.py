from django import forms
from .models import Post
from accounts.models import User, UserProfile
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile 
        fields = ['user_pic', 'address']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ['title', 'picture', 'description']