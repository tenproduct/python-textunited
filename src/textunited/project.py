"""Project related classes."""
from datetime import datetime

from .file import File, FileUpload
from .language import Language


def parse_datetime(value):
    """Convert string to datetime."""
    if not value:
        return None
    try:
        dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    return dt


class Project:
    """Class representing a Text United Project.

    All attributes are stored as python primitives type.
    """

    def __init__(self, client, id_, name, description, creation_date_utc,
                 source_language_id, target_language_id, source_language_code,
                 target_language_code, start_date_utc, end_date_utc, status,
                 owner_id, owner_name, manager_id, manager_name, progress,
                 translation_progress, proofreading_progress,
                 reference_number):
        """Constructor.

        :param client: the Text United client
        :param id_: Project Id in Text United system
        :param name: name of the project
        :param description: description of the project
        :param creation_date_utc: creation time of the project
        :param source_language_id:
        :param target_language_id:
        :param source_language_code:
        :param target_language_code: datetime object with UTC timezone
        :param start_date_utc: When the project starts in UTC hour
        :param end_date_utc: When the project ends in UTC hour
        :param status:
        :param owner_id:
        :param owner_name:
        :param manager_id:
        :param manager_name:
        :param progress:
        :param translation_progress:
        :param proofreading_progress:
        :param reference_number:
        :type client: an object instance of TextUnitedClient
        :type creation_date_utc: datetime object with UTC timezone
        :type start_date_utc: datetime object with UTC timezone
        :type end_date_utc: datetime object with UTC timezone
        """
        self.client = client
        self.id_ = id_
        self.name = name
        self.description = description
        self.creation_date_utc = creation_date_utc
        self.source_language_id = source_language_id
        self.target_language_id = target_language_id
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code
        self.start_date_utc = start_date_utc
        self.end_date_utc = end_date_utc
        self.status = status
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.manager_id = manager_id
        self.manager_name = manager_name
        self.progress = progress
        self.translation_progress = translation_progress
        self.proofreading_progress = proofreading_progress
        self.reference_number = reference_number

    @property
    def source_language(self):
        """Return a Language object with the source language."""
        try:
            source_language = Language(self.source_language_id)
        except ValueError:
            raise NotImplementedError(
                'Language with id {} is not implemented'.format(
                    self.source_language_id
                )
            )
        return source_language

    @property
    def target_language(self):
        """Return a Language object with the target language."""
        try:
            target_language = Language(self.target_language_id)
        except ValueError:
            raise NotImplementedError(
                'Language with id {} is not implemented'.format(
                    self.target_language_id
                )
            )
        return target_language

    def get_files(self):
        """Get a list with all the files that are in the project to translate.

        A project in Text United is composed by a list of files to translate.
        This list contains all files without filtering by status or any #
        attribute.

        :return: a list with an object of each file in the project
        :rtype: a List of File
        """
        self.client.logger.info("Retrieving files for project %s", self.id_)
        files = self.client.fetch_json(
            '/projectfiles?projectId={}'.format(self.id_)
        )

        file_list = [
            File.from_json(
                client=self.client,
                project_id=self.id_,
                json_obj=file)
            for file in files
        ]
        self.client.logger.info(
            "%s files for project %s",
            len(file_list),
            self.id_
        )
        return file_list

    @classmethod
    def from_json(cls, client, json_obj):
        """Deserialize the project json to Project object.

        :param client: an object instance of TextUnitedClient
        :param json_obj: the account json object.
        :type client: TextUnitedClient
        :type json_obj: JSON object
        :return: a Project object with the attributes of the JSON object
        :rtype: Project
        """
        project = cls(
            client=client,
            id_=json_obj['Id'],
            name=json_obj['Name'],
            description=json_obj['Description'],
            creation_date_utc=parse_datetime(json_obj['CreationDateUtc']),
            source_language_id=json_obj['SourceLanguageId'],
            target_language_id=json_obj['TargetLanguageId'],
            source_language_code=json_obj['SourceLanguageCode'],
            target_language_code=json_obj['TargetLanguageCode'],
            start_date_utc=parse_datetime(json_obj['StartDateUtc']),
            end_date_utc=parse_datetime(json_obj['EndDateUtc']),
            status=json_obj['State'],
            owner_id=json_obj['OwnerId'],
            owner_name=json_obj['OwnerName'],
            manager_id=json_obj['ManagerId'],
            manager_name=json_obj['ManagerName'],
            progress=json_obj['Progress'],
            translation_progress=json_obj['TranslationProgress'],
            proofreading_progress=json_obj['ProofreadingProgress'],
            reference_number=json_obj['ReferenceNumber'],
        )
        return project

    def __str__(self):
        """Get string representation of the object."""
        value = (
            'id#{id} "{name}" {source} -> {target} by {owner} ({status})'
        ).format(
            id=self.id_,
            name=self.name,
            source=self.source_language_code,
            target=self.target_language_code,
            owner=self.owner_name,
            status=self.status,
        )
        return value


class ProjectRequest:
    """Class representing a Text United Project Creation request data.

    This class contains all the attributes needed for creating a new project by
    the API. Once created, it is possible to serialize in the API format with
    :func:`to_json`
    """

    def __init__(self, name, source_language, target_language,
                 description, files, translator_id, end_date=None,
                 proofreader_id=None, in_country_reviewer_id=None):
        """Constructor.

        :param name:
        :param source_language:
        :param target_language:
        :param description:
        :param files:
        :param translator_id:
        :param end_date:
        :param proofreader_id:
        :param in_country_reviewer_id:
        :type source_language: An instance of Language
        :type target_language: An instance of Language
        """
        if not all(isinstance(f, FileUpload) for f in files):
            raise TypeError(
                "Could not create ProjectRequest. All objects in `files` "
                "must be FileUpload instance type."
            )

        if not isinstance(source_language, Language):
            raise TypeError(
                "Could not create ProjectRequest. source_language "
                "should be instance of Language"
            )

        if not isinstance(target_language, Language):
            raise TypeError(
                "Could not create ProjectRequest. source_language "
                "should be instance of Language"
            )

        self.name = name
        self.source_language = source_language
        self.target_language = target_language
        self.description = description
        self.files = files
        self.translator_id = translator_id
        self.end_date = end_date
        self.proofreader_id = proofreader_id
        self.in_country_reviewer_id = in_country_reviewer_id

    def __repr__(self):
        """Return the identifier of a project."""
        value = "'{}' {} to {}".format(
            self.name,
            self.source_language.name,
            self.target_language.name
        )
        return value

    def to_json(self):
        """Serialize Project request in Text United API format.

        :return: a JSON Object matching Text United creation format
        :rtype: a JSON Object
        """
        json_obj = {
            'ProjectName': self.name,
            'SourceLanguageId': self.source_language.value,
            'TargetLanguageId': self.target_language.value,
            'Description': self.description,
            'Files': [f.to_json() for f in self.files],
            'TranslatorId': self.translator_id,
            'EndDate': self.end_date.isoformat() if self.end_date else None,
            'ProofreaderId': self.proofreader_id,
            'InCountryReviewerId': self.in_country_reviewer_id
        }
        return json_obj
