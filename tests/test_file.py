"""Test for files."""
import pytest

from textunited.file import File, FileUpload


@pytest.fixture
def mock_file_download_content(mocker):
    """Patch get_translated_content and get_source_content."""
    translated = mocker.patch(
        'textunited.file.File.get_translated_content'
    )
    source = mocker.patch(
        'textunited.file.File.get_source_content'
    )
    return translated, source


@pytest.fixture
def file_factory(client_mock, b64message):
    """Return a file factory."""
    fetch_json, client = client_mock
    decoded, encoded = b64message
    fetch_json.return_value = {'Content': encoded}
    file = File(client, 123, 321, 'Test.txt', None, 12, 12, 'Translated')
    return file, fetch_json, client, decoded


@pytest.mark.parametrize('download_source', [True, False])
@pytest.mark.parametrize('download_translated,status,expected', [
    (True, 'Translated', True),
    (True, 'InProgress', False),
    (False, 'Translated', False),
    (False, 'InProgress', False),
])
def test_file_from_json(
        client_mock, mock_file_download_content, download_source,
        download_translated, status, expected):
    """Test file from_json."""
    mock_translated, mock_source = mock_file_download_content
    json_obj = {
        "FileId": 156148,
        "Filename": "Resources.resx",
        "Subdir": "/important",
        "FileSize": 6991,
        "Words": 28,
        "Status": status
    }
    project_id = 123
    result = File.from_json(
        client_mock,
        project_id,
        json_obj,
        download_translated,
        download_source
    )
    assert isinstance(result, File)
    assert result.client == client_mock
    assert result.project_id == project_id
    assert result.id_ == 156148
    assert result.name == "Resources.resx"
    assert result.subdir == "/important"
    assert result.size == 6991
    assert result.words == 28
    assert result.status == status
    if download_source:
        mock_source.assert_called_once()
    else:
        assert not mock_source.called
    if expected:
        mock_translated.assert_called_once()
    else:
        assert not mock_translated.called
    assert str(result) == (
        'id#156148 "Resources.resx" at project 123 ({})'.format(result.status)
    )


def test_get_translated_content(file_factory):
    """Test get translated content."""
    file, fetch_json, client, decoded = file_factory
    file.get_translated_content()
    assert file.translated_content == decoded
    fetch_json.assert_called_once_with(
        '/projectfiles?projectId=123&fileId=321&type=translated'
    )


def test_get_source_content(file_factory):
    """Test get_source_content."""
    file, fetch_json, client, decoded = file_factory
    file.get_source_content()
    assert file.source_content == decoded
    fetch_json.assert_called_once_with(
        '/projectfiles?projectId=123&fileId=321&type=source'
    )


def test_file_upload_init_only_accepts_bytes_content():
    """Test FileUpload only accepts bytes."""
    with pytest.raises(TypeError):
        FileUpload('fake name', 'fake content')


def test_file_upload_to_json(b64message):
    """Test FileUpload to_json."""
    decoded, encoded = b64message
    file = FileUpload('test.txt', decoded)
    expected_result = {
        'Filename': 'test.txt',
        'Content': encoded
    }
    assert file.to_json() == expected_result
