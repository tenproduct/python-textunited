"""Account related classes."""


class Account:
    """Class representing a TextUnited account.

    All attributes are stored as python primitives type.
    """

    def __init__(
            self, id_, email, first_name, last_name, phone=None,
            position=None):
        """Constructor.

        :param id_: Text United system user id.
        :param email: User email, used for login and notifications in Text
        United.
        :param first_name: First name of user.
        :param last_name: Last name of the user.
        :param phone: User's phone number. It is optional.
        :param position: User's position in the company. It is optional.
        """
        self.id_ = id_
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.position = position

    @classmethod
    def from_json(cls, json_obj):
        """Deserialize the user account json to Account object.

        :param json_obj: the account json object
        :type json_obj: JSON object
        :return: an Account object with the attributes of the JSON object
        :rtype: Account object
        """
        return cls(
            id_=json_obj['Id'],
            email=json_obj['Email'],
            first_name=json_obj['FirstName'],
            last_name=json_obj['LastName'],
            phone=json_obj['Phone'],
            position=json_obj['Position'],
        )

    def __str__(self):
        """Get string representation of the object."""
        return 'id#{} {}'.format(self.id_, self.email)
