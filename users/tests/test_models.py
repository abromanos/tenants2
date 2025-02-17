from unittest.mock import patch
from django.core.exceptions import ValidationError
import pytest

from ..models import JustfixUser, validate_phone_number
from .factories import UserFactory
from onboarding.tests.factories import OnboardingInfoFactory


@pytest.mark.django_db
class TestGenerateRandomUsername:
    def generate(self, prefix='', **kwargs):
        user = JustfixUser.objects.create_user(
            username=JustfixUser.objects.generate_random_username(prefix=prefix),
            **kwargs
        )
        return user

    def test_it_applies_a_prefix_if_provided(self):
        with patch('users.models.get_random_string', side_effect=['boop']):
            assert self.generate(prefix='bleh_').username == 'bleh_boop'

    def test_it_retries_until_a_unique_one_is_found(self):
        with patch('users.models.get_random_string', side_effect=['boop', 'boop', 'blap']):
            user = self.generate(phone_number='1234567890')
            assert user.username == 'boop'
            user2 = self.generate(phone_number='1234567891')
            assert user2.username == 'blap'


def test_formatted_phone_number_works():
    assert JustfixUser().formatted_phone_number() == ''

    user = JustfixUser(phone_number='5551234567')
    assert user.formatted_phone_number() == '(555) 123-4567'

    user = JustfixUser(phone_number='999999999999999999')
    assert user.formatted_phone_number() == '999999999999999999'


@pytest.mark.django_db
def test_admin_url_works():
    user = UserFactory()
    assert user.admin_url == f'https://example.com/admin/users/justfixuser/{user.pk}/change/'


def test_str_works_when_username_is_available():
    user = JustfixUser(username='boop')
    assert str(user) == 'boop'


def test_str_works_when_username_is_unavailable():
    user = JustfixUser()
    assert str(user) == '<unnamed user>'


def test_full_name_only_renders_if_both_first_and_last_are_present():
    user = JustfixUser(first_name='Bobby', last_name='Denver')
    assert user.full_name == 'Bobby Denver'

    assert JustfixUser(first_name='Bobby').full_name == ''
    assert JustfixUser(last_name='Denver').full_name == ''


def test_send_sms_does_nothing_if_user_has_no_onboarding_info(smsoutbox):
    user = JustfixUser(phone_number='5551234500')
    user.send_sms('hello there')
    assert len(smsoutbox) == 0


@pytest.mark.django_db
def test_send_sms_does_nothing_if_user_does_not_allow_it(smsoutbox):
    user = OnboardingInfoFactory(can_we_sms=False).user
    user.send_sms('hello there')
    assert len(smsoutbox) == 0


@pytest.mark.django_db
def test_send_sms_works_if_user_allows_it(smsoutbox):
    user = OnboardingInfoFactory(
        can_we_sms=True, user__phone_number='5551234500').user
    user.send_sms('hello there')
    assert len(smsoutbox) == 1
    assert smsoutbox[0].to == '+15551234500'
    assert smsoutbox[0].body == 'hello there'


@pytest.mark.parametrize('value, excmsg', [
    ('5', 'U.S. phone numbers must be 10 digits.'),
    ('b125551234', 'Phone numbers can only contain digits.'),
    ('1917451234', '191 is an invalid area code.'),
])
def test_validate_phone_number_raises_validation_errors(value, excmsg):
    with pytest.raises(ValidationError) as excinfo:
        validate_phone_number(value)
    assert excinfo.value.args[0] == excmsg


def test_validate_phone_number_works_with_valid_phone_numbers():
    validate_phone_number('4151234567')
