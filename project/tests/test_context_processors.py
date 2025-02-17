import pytest
from django.urls import path
from django.template import RequestContext
from django.template import Template
from django.http import HttpResponse

from project.context_processors import ga_snippet, rollbar_snippet, facebook_pixel_snippet


def show_ga_snippet(request):
    template = Template('{{ GA_SNIPPET }}')
    return HttpResponse(template.render(RequestContext(request)))


def show_facebook_pixel_snippet(request):
    template = Template('{{ FACEBOOK_PIXEL_SNIPPET }}')
    return HttpResponse(template.render(RequestContext(request)))


def show_rollbar_snippet(request):
    template = Template('{{ ROLLBAR_SNIPPET }}')
    return HttpResponse(template.render(RequestContext(request)))


urlpatterns = [
    path('ga', show_ga_snippet),
    path('facebook-pixel', show_facebook_pixel_snippet),
    path('rollbar', show_rollbar_snippet),
]


def test_ga_snippet_is_empty_when_tracking_id_is_not_set(settings):
    assert ga_snippet(None) == {}


def ensure_response_sets_csp(res, *args):
    csp = res['Content-Security-Policy']
    assert f"'unsafe-inline' 'sha256-" in csp
    for arg in args:
        assert arg in csp


@pytest.mark.urls(__name__)
def test_ga_snippet_works(client, settings):
    settings.GA_TRACKING_ID = 'UA-1234'
    res = client.get('/ga')
    assert res.status_code == 200
    html = res.content.decode('utf-8')
    assert 'UA-1234' in html
    ensure_response_sets_csp(res, 'google-analytics.com')


def test_facebook_pixel_snippet_is_empty_when_tracking_id_is_not_set(settings):
    assert facebook_pixel_snippet(None) == {}


@pytest.mark.urls(__name__)
def test_facebook_pixel_snippet_works(client, settings):
    settings.FACEBOOK_PIXEL_ID = '1234567'
    res = client.get('/facebook-pixel')
    assert res.status_code == 200
    html = res.content.decode('utf-8')
    assert '1234567' in html
    ensure_response_sets_csp(res, 'connect.facebook.net')
    ensure_response_sets_csp(res, 'www.facebook.com')


def test_rollbar_snippet_is_empty_when_access_token_is_not_set(settings):
    assert rollbar_snippet(None) == {}


@pytest.mark.urls(__name__)
def test_rollbar_snippet_works(client, settings):
    def get_html():
        res = client.get('/rollbar')
        assert res.status_code == 200
        return (res, res.content.decode('utf-8'))

    settings.ROLLBAR_ACCESS_TOKEN = 'boop'
    res, html = get_html()
    assert 'accessToken: "boop"' in html
    assert 'environment: "production"' in html
    ensure_response_sets_csp(res, 'rollbar.com')

    settings.DEBUG = True
    res, html = get_html()
    assert 'environment: "development"' in html


def test_rollbar_js_url_exists(staticfiles, client):
    url = rollbar_snippet.get_context()['rollbar_js_url']
    res = client.get(url)
    assert res.status_code == 200
    assert res['Content-Type'] == 'application/javascript; charset="utf-8"'
