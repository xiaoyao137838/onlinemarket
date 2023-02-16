from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password']

    def clean(self):
        clean_data = super(UserForm, self).clean()
        password = clean_data['password']
        confirm_password = clean_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('The passwords do not match.')