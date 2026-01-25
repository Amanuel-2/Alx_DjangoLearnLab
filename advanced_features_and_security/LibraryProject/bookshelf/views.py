from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book
from .forms import BookForm


# Security notes:
# - All user input is handled via Django forms (`BookForm`) which validate and
#   clean data. This prevents SQL injection as the ORM is used for queries and
#   no raw SQL or string interpolation is performed.
# - Templates use Django auto-escaping for output. Ensure any rich HTML input
#   is sanitized before rendering.
# - CSRF protection is enforced by including `{% csrf_token %}` in form templates
#   and by `CsrfViewMiddleware` enabled in `settings.py`.


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
	books = Book.objects.all()
	return render(request, 'bookshelf/book_list.html', {'books': books})


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
	book = get_object_or_404(Book, pk=pk)
	return render(request, 'bookshelf/book_detail.html', {'book': book})


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
	if request.method == 'POST':
		form = BookForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('book_list')
	else:
		form = BookForm()
	return render(request, 'bookshelf/book_form.html', {'form': form})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
	book = get_object_or_404(Book, pk=pk)
	if request.method == 'POST':
		form = BookForm(request.POST, instance=book)
		if form.is_valid():
			form.save()
			return redirect('book_detail', pk=book.pk)
	else:
		form = BookForm(instance=book)
	return render(request, 'bookshelf/book_form.html', {'form': form, 'book': book})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
	book = get_object_or_404(Book, pk=pk)
	if request.method == 'POST':
		book.delete()
		return redirect('book_list')
	return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})
