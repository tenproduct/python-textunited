"""Test for account."""
from textunited.account import Account


def test_account_from_json():
    """Test account object creation from a JSON object."""
    json_obj = {
        "Email": "john.doe@example.com",
        "Phone": "+48 32 917 945",
        "Position": "Translator",
        "Id": 111999,
        "FirstName": "John",
        "LastName": "Doe"
    }
    result = Account.from_json(json_obj)
    assert isinstance(result, Account)
    assert result.id_ == 111999
    assert result.email == 'john.doe@example.com'
    assert result.first_name == 'John'
    assert result.last_name == 'Doe'
    assert result.phone == '+48 32 917 945'
    assert result.position == "Translator"
    assert str(result) == 'id#111999 john.doe@example.com'
