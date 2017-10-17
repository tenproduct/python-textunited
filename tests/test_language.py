"""Test for language."""
from textunited.language import Language


def test_allowed_get_language_by_name_different_format():
    """Test that different keys returns the same language."""
    assert Language['es_es'] is Language.es_es
    assert Language['es-es'] is Language.es_es
    assert Language['es_ES'] is Language.es_es
    assert Language['es-ES'] is Language.es_es
