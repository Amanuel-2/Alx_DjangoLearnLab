#!/usr/bin/env python
"""
Sample queries demonstrating Django ORM relationships:
- ForeignKey relationship
- ManyToMany relationship  
- OneToOne relationship
"""

import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing queries"""
    
    # Clear existing data
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George R.R. Martin")
    author3 = Author.objects.create(name="Stephen King")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="A Game of Thrones", author=author2)
    book4 = Book.objects.create(title="A Clash of Kings", author=author2)
    book5 = Book.objects.create(title="The Shining", author=author3)
    book6 = Book.objects.create(title="Carrie", author=author3)
    
    # Create libraries
    central_library = Library.objects.create(name="Central Library")
    downtown_library = Library.objects.create(name="Downtown Library")
    
    # Add books to libraries
    central_library.books.add(book1, book2, book3, book5)
    downtown_library.books.add(book4, book6)
    
    # Create librarians
    Librarian.objects.create(name="Alice Johnson", library=central_library)
    Librarian.objects.create(name="Bob Smith", library=downtown_library)
    
    print("✅ Sample data created successfully!")
    return author1, central_library, downtown_library

def demonstrate_queries():
    """Demonstrate different types of relationship queries"""
    
    print("\n" + "="*60)
    print("DEMONSTRATING DJANGO ORM RELATIONSHIP QUERIES")
    print("="*60)
    
    # Create sample data
    author1, central_library, downtown_library = create_sample_data()
    
    print("\n" + "-"*40)
    print("1. QUERY ALL BOOKS BY A SPECIFIC AUTHOR (ForeignKey)")
    print("-"*40)
    
    # Get author J.K. Rowling
    jk_rowling = Author.objects.get(name="J.K. Rowling")
    
    # Query 1: All books by a specific author using ForeignKey relationship
    # Method 1: Using the reverse relation (related_name='books')
    books_by_rowling = jk_rowling.books.all()
    print(f"Books by {jk_rowling.name}:")
    for book in books_by_rowling:
        print(f"  - {book.title}")
    
    # Method 2: Using filter
    books_by_rowling_alt = Book.objects.filter(author__name="J.K. Rowling")
    print(f"\nSame query using filter (found {books_by_rowling_alt.count()} books):")
    for book in books_by_rowling_alt:
        print(f"  - {book.title}")
    
    print("\n" + "-"*40)
    print("2. LIST ALL BOOKS IN A LIBRARY (ManyToMany)")
    print("-"*40)
    
    # Query 2: All books in a library using ManyToMany relationship
    central_books = central_library.books.all()
    print(f"Books in {central_library.name}:")
    for book in central_books:
        print(f"  - {book.title} (by {book.author.name})")
    
    # Alternative: Find libraries containing a specific book
    harry_potter = Book.objects.get(title__contains="Philosopher")
    libraries_with_harry = harry_potter.libraries.all()
    print(f"\nLibraries with '{harry_potter.title}':")
    for library in libraries_with_harry:
        print(f"  - {library.name}")
    
    print("\n" + "-"*40)
    print("3. RETRIEVE THE LIBRARIAN FOR A LIBRARY (OneToOne)")
    print("-"*40)
    
    # Query 3: Librarian for a library using OneToOne relationship
    # Method 1: Using the reverse relation (related_name='librarian')
    central_librarian = central_library.librarian
    print(f"Librarian for {central_library.name}: {central_librarian.name}")
    
    # Method 2: Direct query
    downtown_librarian = Librarian.objects.get(library=downtown_library)
    print(f"Librarian for {downtown_library.name}: {downtown_librarian.name}")
    
    # Method 3: Using select_related for optimization
    librarian_with_library = Librarian.objects.select_related('library').get(library=central_library)
    print(f"\nUsing select_related - Librarian: {librarian_with_library.name}, Library: {librarian_with_library.library.name}")
    
    print("\n" + "-"*40)
    print("ADDITIONAL RELATIONSHIP QUERIES")
    print("-"*40)
    
    # Additional useful queries
    print("\n4. Find all authors with books in a specific library:")
    authors_in_central = Author.objects.filter(books__libraries=central_library).distinct()
    for author in authors_in_central:
        print(f"  - {author.name}")
    
    print("\n5. Count books by each author in Central Library:")
    from django.db.models import Count
    author_stats = Author.objects.filter(
        books__libraries=central_library
    ).annotate(
        book_count=Count('books')
    )
    for author in author_stats:
        print(f"  - {author.name}: {author.book_count} book(s)")
    
    print("\n6. Libraries without a specific book:")
    libraries_without_game = Library.objects.exclude(books__title__contains="Game")
    for library in libraries_without_game:
        print(f"  - {library.name}")
    
    print("\n✅ All queries demonstrated successfully!")

if __name__ == "__main__":
    demonstrate_queries()