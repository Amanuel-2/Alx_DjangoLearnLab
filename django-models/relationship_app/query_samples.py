#!/usr/bin/env python3
"""
Django ORM Relationship Queries Demonstration
"""

import os
import django
import sys

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')

try:
    django.setup()
    print("Django setup successful!")
except Exception as e:
    print(f"Error setting up Django: {e}")
    sys.exit(1)

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing queries"""
    print("Setting up sample data...")
    
    # Clear existing data (in reverse order to handle foreign key constraints)
    Librarian.objects.all().delete()
    Library.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="J.R.R. Tolkien")
    
    # Create books
    book1 = Book.objects.create(
        title="Harry Potter and the Philosopher's Stone", 
        author=author1
    )
    book2 = Book.objects.create(
        title="Harry Potter and the Chamber of Secrets", 
        author=author1
    )
    book3 = Book.objects.create(title="1984", author=author2)
    book4 = Book.objects.create(title="Animal Farm", author=author2)
    book5 = Book.objects.create(title="The Hobbit", author=author3)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Public Library")
    library2 = Library.objects.create(name="City University Library")
    
    # Add books to libraries (ManyToMany relationship)
    library1.books.add(book1, book2, book3)
    library2.books.add(book3, book4, book5)
    
    # Create librarians (OneToOne relationship)
    Librarian.objects.create(name="Alice Johnson", library=library1)
    Librarian.objects.create(name="Bob Smith", library=library2)
    
    print("Sample data created successfully!\n")
    return True

def demonstrate_queries():
    """Demonstrate the three required relationship queries"""
    
    print("=" * 60)
    print("REQUIRED DJANGO ORM RELATIONSHIP QUERIES")
    print("=" * 60)
    
    # 1. Query all books by a specific author (ForeignKey)
    print("\n1. QUERY ALL BOOKS BY A SPECIFIC AUTHOR")
    print("-" * 40)
    print("All books by J.K. Rowling:")
    try:
        rowling = Author.objects.get(name="J.K. Rowling")
        books_by_rowling = rowling.books.all()  # Using related_name 'books'
        
        if books_by_rowling:
            for book in books_by_rowling:
                print(f"  • {book.title}")
        else:
            print("  No books found for this author")
    except Author.DoesNotExist:
        print("  Author not found")
    except Exception as e:
        print(f"  Error: {e}")
    
    # 2. List all books in a library (ManyToMany)
    print("\n\n2. LIST ALL BOOKS IN A LIBRARY")
    print("-" * 40)
    print("All books in Central Public Library:")
    try:
        central_library = Library.objects.get(name="Central Public Library")
        books_in_library = central_library.books.all()
        
        if books_in_library:
            for book in books_in_library:
                print(f"  • {book.title} by {book.author.name}")
        else:
            print("  No books found in this library")
    except Library.DoesNotExist:
        print("  Library not found")
    except Exception as e:
        print(f"  Error: {e}")
    
    # 3. Retrieve the librarian for a library (OneToOne)
    print("\n\n3. RETRIEVE THE LIBRARIAN FOR A LIBRARY")
    print("-" * 40)
    print("Librarian for Central Public Library:")
    try:
        central_library = Library.objects.get(name="Central Public Library")
        librarian = central_library.librarian  # Using OneToOne related_name
        
        print(f"  Librarian: {librarian.name}")
    except Library.DoesNotExist:
        print("  Library not found")
    except Librarian.DoesNotExist:
        print("  No librarian assigned to this library")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print("QUERY DEMONSTRATION COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    # Create sample data first
    if create_sample_data():
        # Demonstrate required queries
        demonstrate_queries()
