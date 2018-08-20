import pytest

from project.justfix_environment import BASE_DIR
from users.tests.factories import UserFactory
from project.util import schema_json


FRONTEND_QUERY_DIR = BASE_DIR / 'frontend' / 'lib' / 'queries'


def get_frontend_query(filename):
    return (FRONTEND_QUERY_DIR / filename).read_text()


@pytest.mark.django_db
def test_login_works(graphql_client):
    user = UserFactory(phone_number='5551234567', password='blarg')
    result = graphql_client.execute(
        get_frontend_query('LoginMutation.graphql'),
        variable_values={
            'input': {
                'phoneNumber': '5551234567',
                'password': 'blarg'
            }
        }
    )

    login = result['data']['login']
    assert login['errors'] == []
    assert len(login['csrfToken']) > 0
    assert graphql_client.request.user.pk == user.pk


@pytest.mark.django_db
def test_logout_works(graphql_client):
    user = UserFactory()
    graphql_client.request.user = user
    logout_mutation = get_frontend_query('LogoutMutation.graphql')
    result = graphql_client.execute(logout_mutation)

    assert len(result['data']['logout']['csrfToken']) > 0
    assert graphql_client.request.user.pk is None


def test_hello_works_when_logged_out(graphql_client):
    result = graphql_client.execute('query { hello(thing: "BLARG") }')
    assert result['data']['hello'] == \
        'Hello from GraphQL! You passed in "BLARG" and are not logged in'


def test_hello_works_when_logged_in(graphql_client):
    graphql_client.request.user = UserFactory.build()
    result = graphql_client.execute('query { hello(thing: "U") }')
    assert result['data']['hello'] == 'Hello from GraphQL! You passed in "U" and are logged in'


def test_there_works(graphql_client):
    result = graphql_client.execute('query { there }')
    assert result['data']['there'] == 123


def test_schema_json_is_up_to_date():
    err_msg = (
        f'{schema_json.FILENAME} is out of date! '
        f'Please run "{schema_json.REBUILD_CMDLINE}" to rebuild it.'
    )

    if not schema_json.is_up_to_date():
        raise Exception(err_msg)
