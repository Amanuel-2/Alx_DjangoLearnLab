from django.core.management.base import BaseCommand
from relationship_app.models import Author, Book, Library, Librarian

class Command(BaseCommand):
    help = 'Demonstrate Django ORM relationship queries'

    def handle(self, *args, **options):
        self.stdout.write("Demonstrating Django ORM Relationships...")
        
        # Create sample data
        self.create_sample_data()
        
        # Demonstrate queries
        self.demonstrate_queries()
    
    def create_sample_data(self):
        """Create sample data"""
        self.stdout.write("Creating sample data...")
        
        # Clear existing
        Librarian.objects.all().delete()
        Library.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        
        # Create data
        a1 = Author.objects.create(name="J.K. Rowling")
        a2 = Author.objects.create(name="George Orwell")
        
        b1 = Book.objects.create(title="HP 1", author=a1)
        b2 = Book.objects.create(title="HP 2", author=a1)
        b3 = Book.objects.create(title="1984", author=a2)
        
        lib = Library.objects.create(name="Main Library")
        lib.books.add(b1, b2, b3)
        
        Librarian.objects.create(name="Alice", library=lib)
        
        self.stdout.write("Sample data created!")
    
    def demonstrate_queries(self):
        """Demonstrate the three required queries"""
        self.stdout.write("\n" + "="*50)
        self.stdout.write("1. Books by J.K. Rowling:")
        
        rowling = Author.objects.get(name="J.K. Rowling")
        for book in rowling.books.all():
            self.stdout.write(f"  - {book.title}")
        
        self.stdout.write("\n2. Books in Main Library:")
        library = Library.objects.get(name="Main Library")
        for book in library.books.all():
            self.stdout.write(f"  - {book.title}")
        
        self.stdout.write("\n3. Librarian for Main Library:")
        librarian = library.librarian
        self.stdout.write(f"  - {librarian.name}")
