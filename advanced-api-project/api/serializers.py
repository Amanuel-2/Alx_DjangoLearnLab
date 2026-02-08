from rest_framework import serializers
from .models import Author, Book
from datetime import date


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Serializes all fields and validates publication year.
    """

    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, data):
        """
        Ensure publication_year is not in the future.
        """
        current_year = date.today().year
        if data['publication_year'] > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return data

    
class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes related books using a nested serializer.
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']

