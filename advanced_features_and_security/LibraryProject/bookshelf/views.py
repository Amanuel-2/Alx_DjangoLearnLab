from django.shortcuts import render, redirect, get_object_or_404 
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Library, Book  # <-- MUST include Library
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.views.decorators.http import require_POST
from .forms import ExampleForm

from django import forms

# List all books
def list_books(request):
    books = Book.objects.all()  # <-- MUST be exactly this
    return render(request, 'relationship_app/list_books.html', {
        'books': books
    })


# Library detail view
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # <-- MUST match this exactly
    context_object_name = 'library'


# User registration
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# User login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


# User logout
@require_POST
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')


# -----------------------
# Role-Based Access Views
# -----------------------

# Role check functions
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# Admin view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


# Member view
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')



# Simple form for Book creation/editing
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']


# -----------------------
# Add Book
# -----------------------
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})


# -----------------------
# Edit Book
# -----------------------
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})


# -----------------------
# Delete Book
# -----------------------
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})


@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books':books})


@permission_required('relationship_app.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        Book.objects.create(title=title, author=author)
        return redirect('book_list')

    return render(request, 'relationship_app/create_book.html')

@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.save()
        return redirect('book_list')

    return render(request, 'relationship_app/edit_book.html', {'book': book})

@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')

Book.objects.filter(title__icontains=query)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"


def example_form_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = ExampleForm()

    return render(request, "bookshelf/example_form.html", {"form": form}