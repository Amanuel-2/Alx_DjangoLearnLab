import os
import sys
import django

# Fix Python path for standalone script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1️⃣ Query all books by a specific author
author_name = "J.K. Rowling"
try:
    author = Author.objects.get(name=author_name)
    books_by_author = author.books.all()
    print(f"Books by {author_name}: {[book.title for book in books_by_author]}")
except Author.DoesNotExist:
    print(f"No author found with name {author_name}")

# 2️⃣ List all books in a library
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    library_books = library.books.all()
    print(f"Books in {library_name}: {[book.title for book in library_books]}")
except Library.DoesNotExist:
    print(f"No library found with name {library_name}")

# 3️⃣ Retrieve the librarian for a library
try:
    librarian = library.librarian
    print(f"Librarian of {library_name}: {librarian.name}")
except Librarian.DoesNotExist:
    print(f"No librarian assigned for {library_name}")
