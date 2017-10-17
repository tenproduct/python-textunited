"""Custom Exception Classes."""


class ResourceUnavailable(Exception):
    """Exception representing a failed request to a resource."""

    def __init__(self, msg, http_response):
        """Constructor.

        :param msg: Message error
        :param http_response: http response object
        :type http_response: requests.Response
        """
        Exception.__init__(self)
        self._msg = msg
        self._status = http_response.status_code

    def __str__(self):
        """Get string representation of the object."""
        return "{} (HTTP status: {})".format(self._msg, self._status)


class Unauthorized(ResourceUnavailable):
    """Exception representing unauthorized exception."""

    pass


class ProjectNotFound(Exception):
    """Exception representing project not found."""

    pass


class AccountNotFound(Exception):
    """Exception representing account not found."""

    pass
