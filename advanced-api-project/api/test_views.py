from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author
from django.urls import reverse
from datetime import datetime


class BookAPITestCase(APITestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()

        
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

    
        self.book1 = Book.objects.create(title="Alpha Book", publication_year=2020, author=self.author1)
        self.book2 = Book.objects.create(title="Beta Book", publication_year=2023, author=self.author2)

        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update', kwargs={'pk': self.book1.id})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book1.id})
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.id})

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_unauthenticated(self):
        data = {
            "title": "New Book",
            "publication_year": 2024,
            "author": self.author1.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            "title": "New Book",
            "publication_year": datetime.now().year,
            "author": self.author1.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_with_future_year(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            "title": "Future Book",
            "publication_year": datetime.now().year + 1,
            "author": self.author1.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            "title": "Updated Title",
            "publication_year": self.book1.publication_year,
            "author": self.book1.author.id
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url, {'author': self.author1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author1.id)

    def test_search_books_by_title(self):
        response = self.client.get(self.list_url, {'search': 'Alpha'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Alpha" in book["title"] for book in response.data))

    def test_order_books_by_publication_year_desc(self):
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data[0]['publication_year'], response.data[1]['publication_year'])

    def test_permissions_read_only_for_unauthenticated(self):
        # Unauthenticated user can list
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # But cannot create
        data = {
            "title": "No Auth Book",
            "publication_year": 2020,
            "author": self.author1.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
