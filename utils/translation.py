import json
from flask import request

DEFAULT_LANG = "en"

def get_current_lang():
    # Detect language from headers or default
    return request.headers.get("Accept-Language", DEFAULT_LANG).split(",")[0][:2]

def translate_field(field_value, lang=None):
    """
    If field_value is JSON string with translations, return the right one.
    Otherwise return as-is.
    """
    if not lang:
        lang = get_current_lang()

    try:
        translations = json.loads(field_value)
        return translations.get(lang, translations.get(DEFAULT_LANG, field_value))
    except (json.JSONDecodeError, TypeError):
        return field_value
