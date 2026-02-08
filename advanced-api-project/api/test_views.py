from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from api.models import Author, Book


class TestBookAPI(APITestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        #Create author
        self.author = Author.objects.create(name='Fraol M')

        #Create books

        self.book1 = Book.objects.create(
            title='Harry Potter',
            publication_year = 2004,
            author = self.author
        )

        self.book2 = Book.objects.create(
            title='Atomic Habits',
            publication_year = 2001,
            author = self.author
        )

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)    
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter')

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year' : '2022',
            'author': self.author.id
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)   

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')     

        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': '2022',
            'author': self.author.id
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        self.client.login(username="testuser", password="testpass123")

        url = reverse('book-update', args=[self.book1.id])
        data = {
            "title": "Harry Potter Updated",
            "publication_year": 2000,
            "author": self.author.id
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        self.client.login(username="testuser", password="testpass123")

        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_search_books(self):
        url = reverse('book-list') + '?search=Harry'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)