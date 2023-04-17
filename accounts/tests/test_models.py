import pytest
from model_bakery import baker
from pprint import pprint

@pytest.mark.unit
def test_user_str(user):
    assert str(user) == 'xiaoyao'

@pytest.mark.unit
def test_user_get_role(user):
    assert user.get_role() == 'Vendor'

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