from django import forms
from .models import Book


class ExampleForm(forms.ModelForm):
    """
    Example form used to demonstrate secure form handling
    and CSRF protection as required by the task.
    """

    class Meta:
        model = Book
        fields = "__all__"
