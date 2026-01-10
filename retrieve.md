# Retrieve

Command (Django shell):

```python
from bookshelf.models import Book
for book in Book.objects.all():
    print(book.pk, book.title, book.author, book.publication_year)
```

# Expected output (example):

```
1 1984 George Orwell 1949
```
