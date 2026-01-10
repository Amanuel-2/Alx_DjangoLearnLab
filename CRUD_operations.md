# CRUD Operations Transcript

This file contains the actual transcript observed when running the commands in the Django shell.

---

### CREATE

Commands:

```python
from bookshelf.models import Book
b = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
print('CREATED:', b.pk, str(b))
```

Observed output:

```
---CREATE---
CREATED: 1 1984 by George Orwell (1949)
```

---

### RETRIEVE

Commands:

```python
for book in Book.objects.all():
    print(book.pk, book.title, book.author, book.publication_year)
```

Observed output:

```
---RETRIEVE---
1 1984 George Orwell 1949
```

---

### UPDATE

Commands:

```python
b.title = 'Nineteen Eighty-Four'
b.save()
print('UPDATED:', Book.objects.get(pk=b.pk).title)
```

Observed output:

```
---UPDATE---
UPDATED: Nineteen Eighty-Four
```

---

### DELETE

Commands:

```python
b.delete()
print('COUNT_AFTER_DELETE:', Book.objects.count())
```

Observed output:

```
---DELETE---
COUNT_AFTER_DELETE: 0
```
