from django.contrib.auth.models import User
from .models import Review
from rest_framework import status
from rest_framework.test import APITestCase


class ReviewListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_reviews(self):
        adam = User.objects.get(username='adam')
        Review.objects.create(owner=adam, title='a title')
        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_review(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/reviews/', {'title': 'a title'})
        count = Review.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_review(self):
        response = self.client.post('/reviews/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        Review.objects.create(
            owner=adam, title='a title', content='adams content'
        )
        Review.objects.create(
            owner=brian, title='another title', content='brians content'
        )

    def test_can_retrieve_review_using_valid_id(self):
        response = self.client.get('/reviews/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_review_using_invalid_id(self):
        response = self.client.get('/reviews/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_review(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/reviews/1/', {'title': 'a new title'})
        review = Review.objects.filter(pk=1).first()
        self.assertEqual(review.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_review(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/reviews/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)