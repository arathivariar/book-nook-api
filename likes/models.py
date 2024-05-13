from django.db import models
from django.contrib.auth.models import User
from books.models import Book


class Like(models.Model):
    """
    Like model, related to 'owner' and 'book'.
    'owner' is a User instance and 'book' is a Book instance.
    'unique_together' makes sure a user can't like the same book twice.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, related_name='likes', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'book']

    def __str__(self):
        return f'{self.owner} {self.book}'