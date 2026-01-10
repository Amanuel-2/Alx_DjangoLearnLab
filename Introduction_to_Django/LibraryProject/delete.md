# Delete

Command (Django shell):

```python
b = Book.objects.get(pk=1)
b.delete()
print('COUNT_AFTER_DELETE:', Book.objects.count())
```

# Expected output (example):

```
COUNT_AFTER_DELETE: 0
```
