from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    full_name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.full_name

class Book(models.Model):
    """
    Book model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """

    title = models.CharField(max_length=255, blank=False)
    author = models.ManyToManyField(Author)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    language = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False,default="book description")
    image = models.ImageField(
        upload_to='images/', default='../default_post_acvybp', blank=True
    )
    star_rating_1 = models.IntegerField(blank=False, default='1')
    star_rating_2 = models.IntegerField(blank=False, default='2')
    star_rating_3 = models.IntegerField(blank=False, default='3')
    star_rating_4 = models.IntegerField(blank=False, default='4')
    star_rating_5 = models.IntegerField(blank=False, default='5')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'