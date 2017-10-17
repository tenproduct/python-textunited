"""Test client."""
import pytest
from requests.auth import HTTPBasicAuth

from textunited.client import TextUnitedClient
from textunited.exceptions import (
    AccountNotFound,
    ProjectNotFound,
    ResourceUnavailable,
    Unauthorized,
)
from textunited.project import ProjectRequest


@pytest.fixture
def project_from_json_mock(mocker):
    """Patch from_json of project."""
    return mocker.patch('textunited.project.Project.from_json')


def test_text_united_client_constructor(mocker):
    """Test constructor."""
    class MockHTTPBasicAuth(HTTPBasicAuth):

        def __init__(self, *args, **kwargs):
            self.mock = mocker.Mock()
            self.mock(*args, **kwargs)

    mock_auth = mocker.patch('textunited.client.requests.auth')
    mock_auth.HTTPBasicAuth = MockHTTPBasicAuth
    client = TextUnitedClient(company_id=123, api_key='abc')
    assert isinstance(client.auth, MockHTTPBasicAuth)
    client.auth.mock.assert_called_once_with(123, 'abc')


def test_text_united_client_list_projects(client_mock, project_from_json_mock):
    """Test get list of projects."""
    fetch_json, client = client_mock
    client.fetch_json.return_value = ['json_obj1', 'json_obj2']
    project_from_json_mock.side_effect = ['project 1', 'project 2']
    result = client.list_projects()

    client.fetch_json.assert_called_once_with('/projects')
    assert result == ['project 1', 'project 2']
    assert project_from_json_mock.asser_called_once_with()


def test_text_united_client_get_project(client_mock, project_from_json_mock):
    """Test get project."""
    fetch_json, client = client_mock
    result = client.get_project(123)

    fetch_json.assert_called_once_with('/projects/123')
    assert result == project_from_json_mock.return_value
    project_from_json_mock.assert_called_once_with(
        client=client,
        json_obj=fetch_json.return_value
    )


def test_text_united_client_get_project_not_found(client_mock, mocker):
    """Test get_project project not found."""
    fetch_json, client = client_mock
    http_response = mocker.Mock(status_code=400)
    fetch_json.side_effect = ResourceUnavailable('ERROR', http_response)
    with pytest.raises(ProjectNotFound):
        client.get_project(123)


def test_text_united_client_add_project_not_valid_type(mocker, client_mock):
    """Test add_project not valid argument."""
    _, client = client_mock
    with pytest.raises(TypeError):
        client.add_project(mocker.Mock())


def test_text_united_client_add_project(mocker, client_mock):
    """Test add_project."""
    fetch_json, client = client_mock
    project_request = mocker.Mock(spec=ProjectRequest)
    result = client.add_project(project_request)
    assert result == fetch_json.return_value
    fetch_json.assert_called_once_with(
        '/fastproject',
        'POST',
        data=project_request.to_json.return_value
    )


def test_text_united_client_list_accounts(mocker, client_mock):
    """Test list_accounts."""
    fetch_json, client = client_mock
    account_from_json_mock = mocker.patch(
        'textunited.account.Account.from_json'
    )
    fetch_json.return_value = ['1', '2']
    account_from_json_mock.side_effect = ['account 1', 'account 2']
    result = client.list_accounts()

    fetch_json.assert_called_once_with('/employees')
    assert result == ['account 1', 'account 2']
    account_from_json_mock.assert_has_calls([
        mocker.call('1'),
        mocker.call('2')
    ])


def test_text_united_client_get_account(mocker, client_mock):
    """Test get_account found and returned correctly."""
    _, client = client_mock
    account1 = mocker.Mock(email='account1@example.com')
    account2 = mocker.Mock(email='account2@example.com')
    client.list_accounts = mocker.Mock(return_value=[account1, account2])
    result = client.get_account(email='account2@example.com')
    assert result == account2


def test_text_united_client_get_account_not_found(mocker, client_mock):
    """Test get_account not found is raised."""
    _, client = client_mock
    # Not available accounts in TextUnited
    client.list_accounts = mocker.Mock(return_value=[])
    with pytest.raises(AccountNotFound):
        client.get_account(email='account1@example.com')

    # Account not found because doesn't match anyone.
    account1 = mocker.Mock(email='account1@example.com')
    account2 = mocker.Mock(email='account2@example.com')
    client.list_accounts = mocker.Mock(return_value=[account1, account2])
    with pytest.raises(AccountNotFound):
        client.get_account(email='account3@example.com')


@pytest.mark.parametrize('http', ['GET', 'POST', 'PUT'])
@pytest.mark.parametrize(
    'uri,expected_url', [
        ('employee', 'https://www.textunited.com/api/employee'),
        ('/employee', 'https://www.textunited.com/api/employee')
    ]
)
def test_text_united_client_fetch_json(
        mocker, mock_request, client_without_mock, http, uri, expected_url):
    """Test fetch_json."""
    data = mocker.Mock()
    client_without_mock.fetch_json(uri, http_method=http, data=data)

    mock_request.assert_called_once_with(
        http,
        expected_url,
        headers={
            'accept': 'application/json',
            'content-type': 'application/json',
        },
        auth=client_without_mock.auth,
        json=data,
    )


@pytest.mark.parametrize('status_code,exception', [
    (401, Unauthorized, ),
    (404, ResourceUnavailable),
    (500, ResourceUnavailable),
])
def test_text_united_client_fetch_json_errors(
        client_without_mock, mock_request, status_code, exception):
    """Test fetch_json errors."""
    mock_request.return_value.status_code = status_code
    mock_request.return_value.text = 'Error testing'
    with pytest.raises(exception) as e:
        client_without_mock.fetch_json('/employee')
    assert str(e.value) == (
        'Error testing at https://www.textunited.com/api/employee '
        '(HTTP status: {})'.format(status_code)
    )
