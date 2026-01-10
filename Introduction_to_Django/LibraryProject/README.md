# LibraryProject

This is a starter Django project created for learning purposes.

How to run:

1. Create and activate a virtualenv (optional):
   python3 -m venv venv && source venv/bin/activate
2. Install dependencies:
   pip install django
3. Run the development server:
   python manage.py runserver

Project contents:
- `manage.py` - Django management utility
- `LibraryProject/` - project package containing `settings.py`, `urls.py`, and `wsgi/asgi` files

Next steps: create an app (e.g., `books`), add it to INSTALLED_APPS, and start building views and models.