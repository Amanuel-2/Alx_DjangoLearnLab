Bookshelf app permissions and group setup

This app defines custom permissions for the `Book` model and provides a helper management
command to create Groups and assign the appropriate permissions.

Permissions (on model `Book`):
- `can_view`
- `can_create`
- `can_edit`
- `can_delete`

Setup
1. Run migrations to ensure permissions are created:

```bash
python manage.py makemigrations
python manage.py migrate
```

2. Create groups and assign permissions:

```bash
python manage.py create_groups
```

This will create three groups: `Viewers`, `Editors`, and `Admins`.

Group permissions (created by command):
- Viewers: `can_view`
- Editors: `can_view`, `can_create`, `can_edit`
- Admins: all book permissions

Testing
- Create test users and add them to groups via the Django admin.
- Log in as those users and verify access to the views protected by the corresponding
  permissions. Views in `bookshelf/views.py` use `permission_required` decorators:

- `book_list`, `book_detail` -> `bookshelf.can_view`
- `book_create` -> `bookshelf.can_create`
- `book_edit` -> `bookshelf.can_edit`
- `book_delete` -> `bookshelf.can_delete`
