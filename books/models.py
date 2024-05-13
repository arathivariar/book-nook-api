from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """
    Book model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    genre = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    ratings = models.IntegerField(
        choices=RATING_CHOICES, default=0, blank=False)
    image = models.ImageField(
        upload_to='images/', default='../default_post_acvybp', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'