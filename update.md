# Update

Command (Django shell):

```python
b = Book.objects.get(pk=1)
b.title = 'Nineteen Eighty-Four'
b.save()
print('UPDATED:', Book.objects.get(pk=b.pk).title)
```

# Expected output (example):

```
UPDATED: Nineteen Eighty-Four
```
