"""Test for project."""
from datetime import datetime

import pytest

from textunited.file import FileUpload
from textunited.language import Language
from textunited.project import Project, ProjectRequest, parse_datetime


def test_parse_datetime():
    """Test parse datetime."""
    assert parse_datetime(None) is None
    dt = parse_datetime("2016-10-12T22:00:15.085Z")
    assert dt == datetime(2016, 10, 12, 22, 00, 15, 85000)
    dt = parse_datetime("2016-10-12T22:00:15Z")
    assert dt == datetime(2016, 10, 12, 22, 00, 15)


def test_project_from_json(client_mock):
    """Test account object creation from a JSON object."""
    _, client = client_mock
    json_obj = {
        "Description": "Nice Description",
        "CreationDateUtc": "2015-10-12T22:00:15.085Z",
        "EndDateUtc": "2017-10-12T22:00:15.085Z",
        "Id": 8766,
        "ManagerId": 1,
        "ManagerName": "Jon Doe Manager",
        "Name": "WebApplication1",
        "OwnerId": 2,
        "OwnerName": "Jon Doe",
        "Progress": 0,
        "ProofreadingProgress": -1,
        "ReferenceNumber": "ref123",
        "SourceLanguageId": 92,
        "SourceLanguageCode": "PL",
        "StartDateUtc": "2016-10-12T22:00:15.085Z",
        "State": "In progress",
        "TargetLanguageId": 39,
        "TargetLanguageCode": "EN",
        "TranslationProgress": 0
    }
    result = Project.from_json(client, json_obj)
    assert isinstance(result, Project)
    assert result.client == client
    assert result.id_ == 8766
    assert result.name == "WebApplication1"
    assert result.description == "Nice Description"
    assert result.creation_date_utc == (
        datetime(2015, 10, 12, 22, 00, 15, 85000)
    )
    assert result.source_language_id == 92
    assert result.target_language_id == 39
    assert result.source_language_code == 'PL'
    assert result.target_language_code == 'EN'
    assert result.start_date_utc == datetime(2016, 10, 12, 22, 00, 15, 85000)
    assert result.end_date_utc == datetime(2017, 10, 12, 22, 00, 15, 85000)
    assert result.status == "In progress"
    assert result.owner_id == 2
    assert result.owner_name == "Jon Doe"
    assert result.manager_id == 1
    assert result.manager_name == "Jon Doe Manager"
    assert result.progress == 0
    assert result.translation_progress == 0
    assert result.proofreading_progress == -1
    assert result.reference_number == "ref123"
    assert str(result) == (
        'id#8766 "WebApplication1" PL -> EN by Jon Doe (In progress)'
    )


def test_project_get_files(mocker, client_mock):
    """Test get files."""
    fetch_json, client = client_mock
    fetch_json.return_value = ['1', '2', '3']
    file_from_json = mocker.patch('textunited.file.File.from_json')
    file_from_json.side_effect = ['file 1', 'file 2', 'file 3']

    # We don't care for the rest of the attributes
    args = 18 * [None]
    p = Project(client, 358, *args)
    files = p.get_files()
    assert files == ['file 1', 'file 2', 'file 3']
    fetch_json.assert_called_once_with(
        '/projectfiles?projectId=358'
    )
    file_from_json.assert_has_calls([
        mocker.call(client=client, project_id=358, json_obj='1'),
        mocker.call(client=client, project_id=358, json_obj='2'),
        mocker.call(client=client, project_id=358, json_obj='3'),
    ])


def test_source_language_property_valid_id(client_mock):
    """Test source_language_property with a valid id."""
    fetch_json, client = client_mock
    args = 18 * [None]
    p = Project(client, 358, *args)
    p.source_language_id = Language.en_us.value
    assert p.source_language is Language.en_us


def test_source_language_property_not_valid_id(client_mock):
    """Test source_language_property with not valid id."""
    fetch_json, client = client_mock
    args = 18 * [None]
    p = Project(client, 358, *args)
    p.source_language_id = 0
    with pytest.raises(NotImplementedError):
        p.source_language


def test_target_language_property_valid_id(client_mock):
    """Test target_language_property valid id."""
    fetch_json, client = client_mock
    args = 18 * [None]
    p = Project(client, 358, *args)
    p.target_language_id = Language.en_us.value
    assert p.target_language is Language.en_us


def test_target_language_property_not_valid_id(client_mock):
    """Test target_language_property not valid id."""
    fetch_json, client = client_mock
    args = 18 * [None]
    p = Project(client, 358, *args)
    p.target_language_id = 0
    with pytest.raises(NotImplementedError):
        p.target_language


def test_project_request_init_not_valid_file_upload_types(mocker):
    """Test no valid upload file type."""
    files = [mocker.Mock(spec=FileUpload), object()]
    with pytest.raises(TypeError):
        ProjectRequest(
            name='WebApplication1',
            source_language=Language.en_gb,
            target_language=Language.es_es,
            description='Nice description',
            files=files,
            translator_id=1,
        )


def test_project_request_init_not_valid_source_language_types(mocker):
    """Not valid source language type."""
    with pytest.raises(TypeError):
        ProjectRequest(
            name='WebApplication1',
            source_language=12,
            target_language=Language.es_es,
            description='Nice description',
            files=[mocker.Mock(spec=FileUpload)],
            translator_id=1,
        )


def test_project_request_init_not_valid_target_upload_types(mocker):
    """Test not valid target languange."""
    with pytest.raises(TypeError):
        ProjectRequest(
            name='WebApplication1',
            source_language=Language.en_us,
            target_language=12,
            description='Nice description',
            files=[mocker.Mock(spec=FileUpload)],
            translator_id=1,
        )


def test_project_request_to_json(mocker):
    """Test request to JSON."""
    file1 = FileUpload('file 1', b'hello 1')
    file1.to_json = mocker.Mock(return_value='file 1')
    file2 = FileUpload('file 1', b'hello 2')
    file2.to_json = mocker.Mock(return_value='file 2')

    p = ProjectRequest(
        name='WebApplication1',
        source_language=Language.en_gb,
        target_language=Language.es_es,
        description='Nice description',
        files=[file1, file2],
        translator_id=1,
        end_date=datetime(2017, 10, 12, 22, 00, 15, 85000),
        proofreader_id=12,
        in_country_reviewer_id=13,
    )
    json_obj = p.to_json()
    expected_result = {
        'ProjectName': 'WebApplication1',
        'SourceLanguageId': 40,
        'TargetLanguageId': 104,
        'Description': 'Nice description',
        'Files': ['file 1', 'file 2'],
        'TranslatorId': 1,
        'EndDate': '2017-10-12T22:00:15.085000',
        'ProofreaderId': 12,
        'InCountryReviewerId': 13,
    }
    assert json_obj == expected_result
    file1.to_json.assert_called_once()
    file2.to_json.assert_called_once()
