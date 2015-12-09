import os
import json


_cldr_db = None


def get_entry(locale):
    """
    Return a configuration entry for a given locale
    """
    global _cldr_db

    # ensure _rules database is loaded
    if _cldr_db is None:
        with open(get_json_file()) as fd:
            _cldr_db = json.load(fd)

    # take rules for the language we care, or raise KeyError
    lang = locale.replace('-', '_').split('_', 1)[0]
    return _cldr_db[lang]


def get_plural_forms(locale):
    """
    Return a tuple with plural forms (numeric value and plurals expression) for gettext, or raise KeyError

    :rtype: (int, str)
    """
    data = get_entry(locale)  # KeyError here!
    return data['plurals'], '(%s)' % data['formula']


def get_plural_keywords(locale):
    """
    Get the list of plural keywords, allowed for the locale

    :rtype: [str]
    """
    try:
        data = get_entry(locale)
    except KeyError:
        return ['other']
    return data['cases']


def get_json_file():
    """
    Helper function to read CLDR database from a JSON file
    """
    project_root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(project_root, 'data', 'cldr_db.json')
