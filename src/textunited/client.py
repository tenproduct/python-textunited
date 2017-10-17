"""Text United client."""
import logging

import requests

from .account import Account
from .exceptions import (
    AccountNotFound,
    ProjectNotFound,
    ResourceUnavailable,
    Unauthorized,
)
from .project import Project, ProjectRequest


class TextUnitedClient:
    """Base class to communicate with Text United API."""

    logger = logging.getLogger(__name__)

    def __init__(self, company_id, api_key):
        """Constructor.

        It creates a client object
        :param company_id: Company id given by Text United
        :param api_key: Api Key generated in Text United web
        """
        self.auth = requests.auth.HTTPBasicAuth(company_id, api_key)

    def list_projects(self):
        """List with all projects in Text United.

        :return: a list with one object for each project in Text United
        :rtype: list of Project
        """
        self.logger.info("Retrieving all projects")
        json_obj = self.fetch_json('/projects')
        list_projects = [
            Project.from_json(client=self, json_obj=obj)
            for obj in json_obj
        ]
        self.logger.info("%s projects retrieved", len(list_projects))
        return list_projects

    def get_project(self, project_id):
        """Get a project.

        :param project_id: Project id in Text United system.
        :return: an object with all project attributes
        :rtype: Project
        :raises: ProjectNotFound: it is raised when the resource is not
        available or could not been found
        """
        self.logger.info("Retrieving project with id %s", project_id)
        try:
            json_obj = self.fetch_json('/projects/{}'.format(project_id))
        except ResourceUnavailable:
            raise ProjectNotFound(
                'Could not find the project with id {}'.format(project_id)
            )
        project = Project.from_json(client=self, json_obj=json_obj)
        self.logger.info("Project with id %s retrieved", project_id)
        return project

    def add_project(self, project_obj):
        """Add a new project in Text United system.

        :param project_obj: An object with all the attributes needed for
        creating a new Project
        :type project_obj: ProjectRequest
        :return: id of the new created project
        """
        if not isinstance(project_obj, ProjectRequest):
            raise TypeError(
                "Could not create Project. `project_obj must be "
                "ProjectRequest type."
            )
        self.logger.info("Creating project '%s' ", project_obj)
        data = project_obj.to_json()
        project_id = self.fetch_json('/fastproject', 'POST', data=data)
        self.logger.info(
            "Project %s created with id '%s'",
            project_obj,
            project_id
        )
        return project_id

    def list_accounts(self):
        """List with all accounts in Text United system.

        :return: a list with one object for each Account in Text United
        :rtype: list of Account
        """
        self.logger.info("Retrieving all accounts")
        json_obj = self.fetch_json('/employees')
        list_accounts = [Account.from_json(obj) for obj in json_obj]
        self.logger.info("%s accounts retrieved", len(list_accounts))
        return list_accounts

    def get_account(self, email):
        """List with all accounts in Text United system.

        :return: a list with one object for each Account in Text United
        :rtype: list of Account
        :raises: AccountNotFound: it is raised when the resource is not
        available or could not been found
        """
        self.logger.info("Getting account with email %s", email)
        list_account = self.list_accounts()

        if not list_account:
            raise AccountNotFound("Could not find any account in Text United")

        for account in list_account:
            if account.email == email:
                self.logger.info("Account with email %s found")
                return account

        raise AccountNotFound(
            "Could not find an account with email {}".format(email)
        )

    def fetch_json(self, uri_path, http_method='GET', data=None):
        """Perform a request to Text United Server.

        :param uri_path: path to the resource it can be in '/performance' or
        'performance'
        :param http_method: http request type
        :param data: In the case of a POST or a PUT
        :return: request json
        :raises: ResourceUnavailable, Unauthorized
        """
        # set content type and accept headers to handle JSON
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }

        # construct the full URL without query parameters
        if uri_path[0] == '/':
            uri_path = uri_path[1:]
        url = 'https://www.textunited.com/api/{}'.format(uri_path)

        response = requests.request(
            http_method,
            url,
            headers=headers,
            auth=self.auth,
            json=data
        )
        if response.status_code == 401:
            raise Unauthorized("{} at {}".format(response.text, url), response)
        if response.status_code != 200:
            raise ResourceUnavailable(
                "{} at {}".format(response.text, url),
                response
            )

        return response.json()
