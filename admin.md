# Admin configuration for `Book` model

### What was done
- Registered `Book` with the Django admin using `@admin.register(Book)`.
- Created a `BookAdmin` class with the following customizations:
  - `list_display = ('title', 'author', 'publication_year')`
  - `list_filter = ('publication_year', 'author')`
  - `search_fields = ('title', 'author')`

### How to use
1. Ensure migrations have been applied: `python manage.py migrate`
2. Create a superuser: `python manage.py createsuperuser` and follow prompts.
3. Run the development server: `python manage.py runserver`.
4. Open the admin at `http://127.0.0.1:8000/admin/`, log in with the superuser credentials, and manage `Book` entries.
