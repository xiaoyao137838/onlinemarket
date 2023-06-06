import pytest
from model_bakery import baker
from pprint import pprint
from accounts.models import User, UserProfile

def test_user_without_username(db):
    with pytest.raises(ValueError):
        User.objects.create_user(username=None, email='h@gmail.com')

def test_user_without_email(db):
    with pytest.raises(ValueError):
        User.objects.create_user(email=None, username='hh')

def test_create_superuser(db):
    super_user = User.objects.create_superuser(username='super', email='super@gmail.com')
    assert super_user.is_admin
    assert super_user.is_active

@pytest.mark.unit
def test_user_str(user):
    assert str(user) == 'xiaoyao'

@pytest.mark.unit
def test_user_get_role_vendor(user):
    assert user.get_role() == 'Vendor'

@pytest.mark.unit
def test_user_get_role_customer(db):
    customer = User.objects.create(username='xiaoyao', email='a@gmail.com', role=2, password='111111')
    assert customer.get_role() == 'Customer'

@pytest.mark.unit
def test_user_has_perm(user):
    assert user.has_perm('perm') == False

@pytest.mark.unit
def test_has_module_perms(user):
    assert user.has_module_perms('app_label') == True

@pytest.mark.unit
def test_user_is_staff(user):
    assert user.is_staff == False


@pytest.mark.unit
def test_profile_str(user_profile):
    assert str(user_profile) == 'xiaoyao'

@pytest.mark.unit
def test_profile_save(user_profile):
    assert user_profile.location is None
    user_profile.latitude = '102.3'
    user_profile.longitude = '90.8'
    user_profile.save()
    assert user_profile.location is not None

def test_signal(db):
    user = User.objects.create(username='xiaoyao', email='a@gmail.com', role=2, password='111111')
    user_profile = UserProfile.objects.get(user=user)
    user_profile.delete()
    pre_count = UserProfile.objects.count()

    from accounts.signals import post_save_create_userprofile_receiver
    post_save_create_userprofile_receiver(None, user, False)
    cur_count = UserProfile.objects.count()
    assert pre_count == 0
    assert cur_count == 1