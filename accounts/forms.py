from django import forms
from .models import User, UserProfile
from .validators import validate_picture_format

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password']

    def clean(self):
        clean_data = super(UserForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('The passwords do not match.')
        
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    user_pic = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),validators= [validate_picture_format])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),validators= [validate_picture_format])

    class Meta:
        model = UserProfile
        fields = ['user_pic', 'cover_photo', 'address', 'city', 'state', 'country', 'zip_code', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email']