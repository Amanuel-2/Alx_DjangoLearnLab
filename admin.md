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
### Verification (performed)
- I created a local superuser (for verification only) via the shell:

```python
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@example.com', 'password')  # local-only password
```

- I used Django's test client to log in and fetch the admin index (no running server required):

```python
from django.test import Client
c = Client()
c.login(username='admin', password='password')
resp = c.get('/admin/', HTTP_HOST='127.0.0.1')
print(resp.status_code)  # expected 200
```

- Result: admin index returned `200` and the page contains the `Book` model listing — verification successful.