from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create an author
        self.author = Author.objects.create(name='J.K. Rowling')

        # Create a sample book
        self.book = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            author=self.author,
            publication_year=1997
        )
        self.book_url = reverse('book-detail', kwargs={'pk': self.book.id})

    def test_create_book(self):
        url = reverse('book-create')
        data = {'title': 'New Book', 'author': self.author.id, 'publication_year': 2021}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_retrieve_book(self):
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book(self):
        url = reverse('book-update', kwargs={'pk': self.book.id})
        data = {'title': 'Updated Book Title', 'author': self.author.id, 'publication_year': 1998}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book Title')

    def test_delete_book(self):
        url = reverse('book-delete', kwargs={'pk': self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_filter_books_by_title(self):
        url = reverse('book-list') + '?title=Harry Potter'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_author(self):
        url = reverse('book-list') + '?search=Rowling'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books_by_publication_year(self):
        # Create another book for ordering test
        Book.objects.create(title='Newer Book', author=self.author, publication_year=2005)
        url = reverse('book-list') + '?ordering=publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 1997)  # Oldest book first

    def test_permission_denied_for_unauthenticated_user(self):
        self.client.logout()
        url = reverse('book-create')
        data = {'title': 'Unauthorized Book', 'author': self.author.id, 'publication_year': 2023}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
