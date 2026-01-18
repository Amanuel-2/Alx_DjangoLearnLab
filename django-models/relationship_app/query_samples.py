import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing"""
    print("Creating sample data...")
    
    # Clear existing data
    Author.objects.all().delete()
    
    # Create authors
    a1 = Author.objects.create(name="J.K. Rowling")
    a2 = Author.objects.create(name="George Orwell")
    a3 = Author.objects.create(name="J.R.R. Tolkien")
    
    # Create books
    b1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=a1)
    b2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=a1)
    b3 = Book.objects.create(title="1984", author=a2)
    b4 = Book.objects.create(title="Animal Farm", author=a2)
    b5 = Book.objects.create(title="The Hobbit", author=a3)
    
    # Create libraries
    lib1 = Library.objects.create(name="Central Public Library")
    lib2 = Library.objects.create(name="University Library")
    
    # Add books to libraries
    lib1.books.add(b1, b2, b3)
    lib2.books.add(b4, b5, b2)  # b2 is in both libraries
    
    # Create librarians
    Librarian.objects.create(name="Alice Johnson", library=lib1)
    Librarian.objects.create(name="Bob Smith", library=lib2)
    
    print("Sample data created!\n")

def demonstrate_queries():
    """Demonstrate the required relationship queries"""
    
    print("=" * 60)
    print("DJANGO ORM RELATIONSHIP QUERIES DEMONSTRATION")
    print("=" * 60)
    
    # 1. Query all books by a specific author
    print("\n1. QUERY ALL BOOKS BY A SPECIFIC AUTHOR (ForeignKey)")
    print("-" * 40)
    print("Books by J.K. Rowling:")
    try:
        rowling = Author.objects.get(name="J.K. Rowling")
        for book in rowling.books.all():
            print(f"  - {book.title}")
    except Author.DoesNotExist:
        print("  Author not found")
    
    # 2. List all books in a library
    print("\n\n2. LIST ALL BOOKS IN A LIBRARY (ManyToMany)")
    print("-" * 40)
    print("Books in Central Public Library:")
    try:
        library = Library.objects.get(name="Central Public Library")
        for book in library.books.all():
            print(f"  - {book.title} (by {book.author.name})")
    except Library.DoesNotExist:
        print("  Library not found")
    
    # 3. Retrieve the librarian for a library
    print("\n\n3. RETRIEVE THE LIBRARIAN FOR A LIBRARY (OneToOne)")
    print("-" * 40)
    print("Librarian for Central Public Library:")
    try:
        library = Library.objects.get(name="Central Public Library")
        librarian = library.librarian
        print(f"  {librarian.name}")
    except Library.DoesNotExist:
        print("  Library not found")
    except Librarian.DoesNotExist:
        print("  No librarian assigned to this library")
    
    # Bonus: Additional queries
    print("\n\n4. ADDITIONAL DEMONSTRATIONS")
    print("-" * 40)
    
    # Show that a book can be in multiple libraries
    print("Demonstrating ManyToMany - Book in multiple libraries:")
    try:
        book2 = Book.objects.get(title="Harry Potter and the Chamber of Secrets")
        libraries = book2.libraries.all()
        print(f"  '{book2.title}' is available in:")
        for lib in libraries:
            print(f"    - {lib.name}")
    except Book.DoesNotExist:
        print("  Book not found")
    
    # Count books per author
    print("\nCounting books per author:")
    for author in Author.objects.all():
        count = author.books.count()
        print(f"  {author.name}: {count} book(s)")

if __name__ == "__main__":
    create_sample_data()
    demonstrate_queries()
    