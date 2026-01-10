# Create

Command (Django shell):

```python
from bookshelf.models import Book
b = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
print('CREATED:', b.pk, str(b))
```

# Expected output (example):

```
CREATED: 1 1984 by George Orwell (1949)
```
