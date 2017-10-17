"""Text client calls."""
import pytest

import textunited
from textunited.language import Language
from textunited.project import Project


@pytest.fixture
def client():
    """Create client instance."""
    return textunited.TextUnitedClient('123', 'abc')


def test_get_projects(
        mock_request, client, data_list_projects, data_list_files, b64message):
    """Test get project."""
    mock_request.return_value.json.return_value = data_list_projects
    projects = client.list_projects()
    assert len(projects) == 2
    decoded, encoded = b64message
    mock_request.return_value.json.side_effect = [
        data_list_files,
        {'Content': encoded},
    ]
    files = projects[0].get_files()
    assert len(files) == 2
    assert files[0].translated_content == decoded
    assert files[1].translated_content is None


def test_get_accounts(mock_request, client, data_list_accounts):
    """Test get accounts."""
    mock_request.return_value.json.return_value = data_list_accounts
    accounts = client.list_accounts()
    assert len(accounts) == 2


def test_get_project(mock_request, client, data_list_projects):
    """Test get project."""
    mock_request.return_value.json.return_value = data_list_projects[0]
    project = client.get_project(8766)
    assert isinstance(project, Project)


def test_add_project(mock_request, client):
    """Test add project."""
    mock_request.return_value.json.return_value = '1232'
    file = textunited.FileUpload('name.txt', b'hello')
    project = textunited.ProjectRequest(
        'project test',
        Language.en_gb,
        Language.en_us,
        'this a description',
        [file],
        2,
    )
    project_id = client.add_project(project)
    assert project_id == '1232'
