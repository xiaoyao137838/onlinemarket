import tempfile
from django.test import SimpleTestCase, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.forms import UserForm, UserProfileForm, UserInfoForm

class TestForms(TestCase):

    def test_user_form_valid_data(self):
        form = UserForm(data={
       
            'username': 'form_user',
            'email': 'hh@gmail.com',
            'password': '111111',
            'confirm_password': '111111',
            'phone': '123'
        })

        self.assertTrue(form.is_valid())

    def test_user_form_invalid_clean(self):
        form = UserForm(data={
       
            'username': 'form_user',
            'email': 'hh@gmail.com',
            'password': '111111',
            'confirm_password': '119111',
            'phone': '123'
        })

        self.assertFalse(form.is_valid())

    def test_user_form_no_dada(self):
        form = UserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_user_profile_form(self):
        form = UserProfileForm(data={
            'address': 'new address'
        },
        files={
            'user_pic': SimpleUploadedFile("file.jpg", b"file_content"),
            'cover_photo': SimpleUploadedFile("file.jpg", b"file_content")
        })

        self.assertTrue(form.is_valid())

    def test_user_profile_form_init(self):
        form = UserProfileForm(data={
            'address': 'new address',
            'latitude': '112.9',
            'longitude': '44.8'
        },
        files={
            'user_pic': SimpleUploadedFile("file.jpg", b"file_content"),
            'cover_photo': SimpleUploadedFile("file.jpg", b"file_content")
        })
        for field in form.fields:
            if field == 'latitude' or field == 'longitude':
                assert form.fields[field].widget.attrs['readonly'] == 'readonly'

    def test_user_profile_form_no_dada(self):
        form = UserProfileForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)   

    def test_user_info_valid_data(self):
        form = UserInfoForm(data={'email': 'gg@gmail.com'})
        self.assertTrue(form.is_valid())
        
    def test_user_info_form_no_dada(self):
        form = UserInfoForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)   
