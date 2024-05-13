from django.contrib.auth.models import User
from .models import Book
from rest_framework import status
from rest_framework.test import APITestCase


class BookListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_books(self):
        adam = User.objects.get(username='adam')
        Book.objects.create(owner=adam, title='a title')
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_book(self):
        self.client.login(username='adam', password='pass')
        response = self.client.book('/books/', {'title': 'a title'})
        count = Book.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_book(self):
        response = self.client.book('/books/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)