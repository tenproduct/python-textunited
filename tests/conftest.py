"""Fixtures and mock."""
import pytest

from textunited.client import TextUnitedClient


@pytest.fixture
def mock_request(mocker):
    """Mock requests in client file."""
    request = mocker.patch('textunited.client.requests.request')
    request.return_value.status_code = 200
    return request


@pytest.fixture
def client_without_mock(mocker):
    """Return a TextUnitedClient instance without any patch."""
    c = TextUnitedClient(company_id=123, api_key='abc')
    c.auth = mocker.Mock()
    return c


@pytest.fixture
def mock_fetch_json(mocker):
    """Mock fetch_json method of TextUnitedClient."""
    return mocker.patch('textunited.client.TextUnitedClient.fetch_json')


@pytest.fixture
def client_mock(mock_fetch_json):
    """Return a TextUnitedClient instance with the fetch_json mocked."""
    return mock_fetch_json, TextUnitedClient(company_id=123, api_key='abc')


@pytest.fixture
def b64message():
    """Return a message and the b64message of that message."""
    return b'hello_world', 'aGVsbG9fd29ybGQ='


@pytest.fixture
def data_list_projects():
    """Return a JSON list valid project."""
    return [
        {
            "Description": "",
            "CreationDateUtc": "2015-10-12T22:00:15.085Z",
            "EndDateUtc": "2015-10-13T20:00:15.085199Z",
            "Id": 8766,
            "ManagerId": 1,
            "ManagerName": "Jon Doe",
            "Name": "WebApplication1",
            "OwnerId": 1,
            "OwnerName": "Jon Doe",
            "Progress": 0,
            "ProofreadingProgress": -1,
            "ReferenceNumber": "",
            "SourceLanguageId": 92,
            "SourceLanguageCode": "PL",
            "StartDateUtc": "2015-10-12T20:00:15.085199Z",
            "State": "In progress",
            "TargetLanguageId": 39,
            "TargetLanguageCode": "EN",
            "TranslationProgress": 0
        },
        {
            "Description": "",
            "CreationDateUtc": "2015-10-12T22:00:21.528Z",
            "EndDateUtc": "2015-10-13T20:00:21.52801Z",
            "Id": 8767,
            "ManagerId": 1,
            "ManagerName": "Jon Doe",
            "Name": "WebApplication1",
            "OwnerId": 1,
            "OwnerName": "Jon Doe",
            "Progress": 0,
            "ProofreadingProgress": -1,
            "ReferenceNumber": "",
            "SourceLanguageId": 92,
            "SourceLanguageCode": "PL",
            "StartDateUtc": "2015-10-12T20:00:21.52801Z",
            "State": "In progress",
            "TargetLanguageId": 52,
            "TargetLanguageCode": "KA",
            "TranslationProgress": 0
        }
    ]


@pytest.fixture
def data_list_accounts():
    """Return a JSON list valid accounts."""
    return [
        {
            "Email": "john.doe@example.com",
            "Phone": "+48 32 917 947",
            "Position": "System admin",
            "Id": 111999,
            "FirstName": "John",
            "LastName": "Doe"
        },
        {
            "Email": "jane.doe@example.com",
            "Phone": "",
            "Position": None,
            "Id": 112000,
            "FirstName": "Jane",
            "LastName": "Doe"
        }
    ]


@pytest.fixture
def data_list_files():
    """Return a JSON list valid files."""
    return [
        {
            "FileId": 156148,
            "Filename": "Resources.resx",
            "Subdir": "",
            "FileSize": 6991,
            "Words": 28,
            "Status": "Translated"
        },
        {
            "FileId": 156155,
            "Filename": "test.xml",
            "Subdir": "subdir\\subdir2\\target\\",
            "FileSize": 620897,
            "Words": 1066,
            "Status": "Preprocessed"
        }
    ]
