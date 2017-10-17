"""Language Classes."""
import enum


class MetaLanguage(enum.EnumMeta):
    """Custom EnumMeta for Language."""

    def __getitem__(self, name):
        """Override __getitem to allow to find en-gb or en_gb."""
        name = name.lower()
        try:
            return super().__getitem__(name)
        except KeyError:
            return super().__getitem__(name.replace('-', '_'))


class Language(enum.IntEnum, metaclass=MetaLanguage):
    """Supported languages in BCP 47 format.

    It is possible to access to an specific language with `Language['en_gb']`
    or with `Language['en-gb']`.
    """

    ar_ae = 21  # Arabic (United Arab Emirates)
    de_de = 53  # German (Germany)
    en_ca = 158  # English (CA)
    en_gb = 40  # English (UK)
    en_us = 41  # English (US)
    es_co = 108  # Spanish (Colombia)
    es_es = 104  # Spanish (Spain)
    fr_ca = 48  # French (Canada)
    ja = 72  # Japanese
    ko = 76  # Korean
    pt_br = 94  # Portuguese (Brazil)
    zh_hant = 33  # Chinese (Traditional)
    zn_hans = 32  # Chinese (Simplified)
