import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def get_entry():
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open("entries/css.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

get_entry()