import pytest
from users.tests.factories import UserFactory


def execute_mutation(graphql_client, input):
    input = {'other': '', **input}
    return graphql_client.execute(
        """
        mutation MyMutation($input: IssueAreaInput!) {
            issueArea(input: $input) {
                errors {
                    field
                    messages
                }
                session {
                    issues
                    customIssues {
                        area
                        description
                    }
                }
            }
        }
        """,
        variables={'input': input}
    )['data']['issueArea']


@pytest.mark.django_db
def test_issue_area_works(graphql_client):
    graphql_client.request.user = UserFactory.create()

    result = execute_mutation(graphql_client, {
        'area': 'HOME',
        'issues': ['HOME__RATS'],
        'other': 'boop'
    })
    assert result['errors'] == []
    assert result['session']['issues'] == ['HOME__RATS']
    assert result['session']['customIssues'] == [{'area': 'HOME', 'description': 'boop'}]

    result = execute_mutation(graphql_client, {'area': 'HOME', 'issues': []})
    assert result['errors'] == []
    assert result['session']['issues'] == []
    assert result['session']['customIssues'] == []


def test_issue_area_requires_auth(graphql_client):
    result = execute_mutation(graphql_client, {'area': 'HOME', 'issues': ['HOME__RATS']})
    assert result['errors'] == [{'field': '__all__', 'messages': [
        'You do not have permission to use this form!'
    ]}]


def test_issues_is_empty_when_unauthenticated(graphql_client):
    result = graphql_client.execute('query { session { issues, customIssues { area } } }')
    assert result['data']['session']['issues'] == []
    assert result['data']['session']['customIssues'] == []
