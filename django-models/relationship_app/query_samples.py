"""
query_samples.py

Sample Django ORM queries demonstrating relationships.

Usage:
 - Ensure your project's settings module is available via the
   DJANGO_SETTINGS_MODULE environment variable (e.g. export DJANGO_SETTINGS_MODULE=LibraryProject.settings)
 - Run with the Django project root on PYTHONPATH, for example:
     python manage.py shell < relationship_app/query_samples.py
   or run standalone after setting DJANGO_SETTINGS_MODULE and calling django.setup().
"""

import os
import django
from typing import List


def setup_django():
    if 'DJANGO_SETTINGS_MODULE' not in os.environ:
        raise RuntimeError('Please set DJANGO_SETTINGS_MODULE to your project settings before running this script')
    django.setup()


def books_by_author(author_name: str) -> List[str]:
    from .models import Author
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        return []
    return [b.title for b in author.books.all()]


def books_in_library(library_name: str) -> List[str]:
    from .models import Library
    try:
        lib = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return []
    return [b.title for b in lib.books.all()]


def librarian_for_library(library_name: str):
    from .models import Library
    try:
        lib = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return None
    # Using the OneToOne related_name 'librarian'
    return getattr(lib, 'librarian', None)


if __name__ == '__main__':
    setup_django()
    # Example output when invoked directly. Replace names as needed.
    print('Books by author "Jane Doe":', books_by_author('Jane Doe'))
    print('Books in library "Central":', books_in_library('Central'))
    print('Librarian for "Central":', librarian_for_library('Central'))
