import pytest

from users.models import JustfixUser
from users.tests.factories import UserFactory
from project.tests.util import strip_locale
from loc.admin import (
    LetterRequestInline, print_loc_envelopes, get_lob_nomail_reason)
from loc.admin_views import LocAdminViews
from loc.models import LetterRequest, LOC_MAILING_CHOICES
from . import test_lob_api
from .test_views import requires_pdf_rendering
from .factories import (
    LandlordDetailsFactory, LetterRequestFactory, create_user_with_all_info)


def test_loc_actions_shows_text_when_user_has_no_letter_request():
    lr = LetterRequest()
    assert LetterRequestInline.loc_actions(None, lr) == (
        'This user has not yet completed the letter of complaint process.'
    )


@pytest.mark.django_db
def test_loc_actions_shows_pdf_link_when_user_has_letter_request():
    user = UserFactory()
    lr = LetterRequest(user=user)
    lr.save()
    assert f'/loc/admin/{user.pk}/letter.pdf' in LetterRequestInline.loc_actions(None, lr)


@pytest.mark.django_db
def test_print_loc_envelopes_works():
    user = UserFactory()
    redirect = print_loc_envelopes(None, None, JustfixUser.objects.all())
    url = strip_locale(redirect.url)
    assert url == f'/loc/admin/envelopes.pdf?user_ids={user.pk}'


class TestLobIntegrationField:
    def lob_integration(self, obj):
        return LetterRequestInline.lob_integration(None, obj)

    def test_it_returns_info_when_already_mailed(self):
        lr = LetterRequest()
        lr.lob_letter_object = test_lob_api.get_sample_letter()
        assert self.lob_integration(lr) == (
            'The letter was <a href="https://dashboard.lob.com/#/letters/ltr_4868c3b754655f90" '
            'rel="noreferrer noopener" target="_blank">'
            'sent via Lob</a> with the tracking number 9407300000000000000004 and has an '
            'expected delivery date of 2017-09-12.'
        )

    def test_it_returns_button_when_it_can_be_mailed(self, monkeypatch, db):
        lr = LetterRequestFactory()
        monkeypatch.setattr('loc.admin.get_lob_nomail_reason', lambda _: None)
        assert self.lob_integration(lr) == (
            f'<a class="button" href="/admin/lob/{lr.pk}/">'
            'Mail letter of complaint via Lob&hellip;</a>'
        )

    def test_it_returns_reason_when_it_cannot_be_mailed(self):
        assert self.lob_integration(LetterRequest()) == \
            'Unable to send mail via Lob because Lob integration is disabled.'


@pytest.fixture
def enable_lob(settings):
    settings.LOB_SECRET_API_KEY = 'mysecret'
    settings.LOB_PUBLISHABLE_API_KEY = 'mypub'


def create_valid_letter_request():
    user = create_user_with_all_info()
    return LetterRequestFactory(user=user)


class TestCreateMailConfirmationContext:
    deliverable = test_lob_api.get_sample_verification(deliverability='deliverable')
    deliverable_incorrect_unit = test_lob_api.get_sample_verification(
        deliverability='deliverable_incorrect_unit')
    undeliverable = test_lob_api.get_sample_verification(deliverability='undeliverable')

    def create(self, landlord_verification, user_verification):
        return LocAdminViews(None)._create_mail_confirmation_context(
            landlord_verification,
            user_verification
        )

    @pytest.mark.parametrize('landlord,user,expected', [
        [deliverable, undeliverable, False],
        [undeliverable, deliverable, False],
        [undeliverable, undeliverable, False],
        [deliverable_incorrect_unit, deliverable, True],
        [deliverable, deliverable, True]
    ])
    def test_is_deliverable_works(self, landlord, user, expected):
        assert self.create(landlord, user)['is_deliverable'] is expected

    @pytest.mark.parametrize('landlord,user,expected', [
        [deliverable, undeliverable, False],
        [undeliverable, deliverable, False],
        [deliverable_incorrect_unit, deliverable, False],
        [deliverable, deliverable, True]
    ])
    def test_is_definitely_deliverable_works(self, landlord, user, expected):
        assert self.create(landlord, user)['is_definitely_deliverable'] is expected


class TestMailViaLob:
    @pytest.fixture(autouse=True)
    def setup_fixtures(self, db, enable_lob):
        self.lr = create_valid_letter_request()
        self.url = f'/admin/lob/{self.lr.pk}/'

    def test_get_works(self, admin_client, requests_mock):
        requests_mock.post(
            test_lob_api.LOB_VERIFICATIONS_URL,
            json=test_lob_api.get_sample_verification()
        )
        res = admin_client.get(self.url)
        assert res.status_code == 200
        assert b'Mail it with Lob!' in res.content

    @requires_pdf_rendering
    def test_post_works(self, admin_client, requests_mock):
        signed_verifications = LocAdminViews(None)._create_mail_confirmation_context(
            landlord_verification=test_lob_api.get_sample_verification(),
            user_verification=test_lob_api.get_sample_verification()
        )['signed_verifications']
        requests_mock.post(
            test_lob_api.LOB_LETTERS_URL,
            json=test_lob_api.get_sample_letter()
        )
        res = admin_client.post(
            self.url,
            data={'signed_verifications': signed_verifications}
        )
        assert res.status_code == 200
        assert b'Hooray, the letter was sent via Lob' in res.content
        self.lr.refresh_from_db()
        assert self.lr.lob_letter_object['carrier'] == 'USPS'


class TestGetLobNomailReason:
    def test_it_works_when_lob_integration_is_disabled(self):
        assert get_lob_nomail_reason(LetterRequest()) == 'Lob integration is disabled'

    def test_it_works_when_letter_has_no_pk(self, enable_lob):
        assert get_lob_nomail_reason(LetterRequest()) == 'the letter has not yet been created'

    def test_it_works_when_letter_has_already_been_sent(self, enable_lob, db):
        lr = LetterRequestFactory(lob_letter_object={'blah': 1})
        assert get_lob_nomail_reason(lr) == 'the letter has already been sent via Lob'

    def test_it_works_when_user_mails_letter_themselves(self, enable_lob, db):
        lr = LetterRequestFactory(mail_choice=LOC_MAILING_CHOICES.USER_WILL_MAIL)
        assert get_lob_nomail_reason(lr) == \
            'the user wants to mail the letter themself'

    def test_it_works_when_user_has_no_landlord_details(self, enable_lob, db):
        lr = LetterRequestFactory()
        assert get_lob_nomail_reason(lr) == 'the user does not have landlord details'

    def test_it_works_when_user_has_no_onboarding_info(self, enable_lob, db):
        lr = LetterRequestFactory()
        LandlordDetailsFactory(user=lr.user)
        assert get_lob_nomail_reason(lr) == 'the user does not have onboarding info'

    def test_it_returns_none_when_letter_can_be_mailed_via_lob(self, enable_lob, db):
        assert get_lob_nomail_reason(create_valid_letter_request()) is None
