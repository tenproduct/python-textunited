"""File related classes."""
import base64


class File:
    """Class representing each of the files in Text United System.

    In this class we represent each file in Text United. For example, a source
    file and translation file and other attributes as the subdir or status.

    The translated_content and the source_content, both bytes, are get with
    :func:`get_translated_content` and :func:`get_source_content` and saved in
    the object attributes.
    """

    def __init__(self, client, project_id, id_, name, subdir, size, words,
                 status):
        """Constructor.

        :param client: An object instance of TextUnitedClient
        :param project_id: Project Id in Text United system
        :param id_: File Id in Text United system
        :param name: Name of the file
        :param subdir: The path inside the project to the file
        :param size: Size of the file in bytes
        :param words: Number of words for translations
        :param status: string with the status of the file. Possible statuses
        Waiting, ProcessingError, NotTranslated, Translated, TranslationError.
        :type client: an object instance of TextUnitedClient
        """
        self.client = client
        self.project_id = project_id
        self.id_ = id_
        self.name = name
        self.subdir = subdir
        self.size = size
        self.words = words
        self.status = status
        self.translated_content = None
        self.source_content = None

    def get_translated_content(self):
        """Get and save inside the object the translated file content."""
        self.client.logger.info(
            "Retrieving translated content of file %s",
            self
        )

        url = (
            '/projectfiles?projectId={project_id}&fileId={file_id}'
            '&type=translated'
        ).format(project_id=self.project_id, file_id=self.id_)

        json_obj = self.client.fetch_json(url)
        self.translated_content = base64.b64decode(json_obj['Content'])
        self.client.logger.info("Retrieved translated content of file %s", self)

    def get_source_content(self):
        """Get and save inside the object the source file content."""
        self.client.logger.info("Retrieving source content of file %s", self)
        url = (
            '/projectfiles?projectId={project_id}&fileId={file_id}&type=source'
        ).format(project_id=self.project_id, file_id=self.id_)

        json_obj = self.client.fetch_json(url)
        self.source_content = base64.b64decode(json_obj['Content'])
        self.client.logger.info("Retrieved source content of file %s", self)

    @classmethod
    def from_json(cls, client, project_id, json_obj,
                  download_translations=True, download_sources=False):
        """Deserialize the file JSON to File object.

        :param client: an object instance of TextUnitedClient
        :type client: TextUnitedClient
        :param project_id: The project id of the file
        :param json_obj: the File json object
        :param download_translations: a boolean to select to download the
        translated file content. Only if the file status is Translated.
        :param download_sources: a boolean to select to download the source
        file content.
        :type download_translations: bool
        :type download_sources: bool
        :return: a File object with the attributes of the JSON object
        :rtype: File object
        """
        obj = cls(
            client=client,
            project_id=project_id,
            id_=json_obj['FileId'],
            name=json_obj['Filename'],
            subdir=json_obj['Subdir'],
            size=json_obj['FileSize'],
            words=json_obj['Words'],
            status=json_obj['Status'],
        )
        if download_translations and obj.status == 'Translated':
            obj.get_translated_content()
        if download_sources:
            obj.get_source_content()
        return obj

    def __repr__(self):
        """Get string representation of the object."""
        return 'id#{} "{}" at project {} ({})'.format(
            self.id_,
            self.name,
            self.project_id,
            self.status,
        )

    def __str__(self):
        """Get string representation of the object."""
        return 'id#{} "{}" at project {} ({})'.format(
            self.id_,
            self.name,
            self.project_id,
            self.status,
        )


class FileUpload:
    """Class representing a Text United File Upload request data.

    This class contains all the attributes needed for uploading a new file to
    Text United. All files are only possible to upload on the Project creation
    time.
    """

    def __init__(self, name, content):
        """Constructor.

        :param name: File name
        :param content: The file content to be uploaded
        :type name: str
        :type content: bytes
        """
        if not isinstance(content, bytes):
            raise TypeError('content attribute should be bytes type')

        self.name = name
        self.content = content

    def to_json(self):
        """Serialize FileUpload request in Text United API format.

        :return: a JSON Object matching Text United file representation format
        with the content encoded in base64.
        :rtype: a JSON Object
        """
        json_obj = {
            'Filename': self.name,
            'Content': str(base64.b64encode(self.content), 'utf-8'),
        }

        return json_obj
