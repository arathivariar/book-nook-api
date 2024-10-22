from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from booknook_api.permissions import IsOwnerOrReadOnly
from .models import Book, Author, Genre
from .serializers import AuthorSerializer, BookSerializer, GenreSerializer
from .filters import BookFilter


class BookList(generics.ListCreateAPIView):
    """
    List books or create a book if logged in
    The perform_create method associates the book with the logged in user.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all().order_by('-created_at')
    filterset_class = BookFilter
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
        'author',
        'genre',
    ]
    ordering_fields = [
        'title',
        'created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetail(generics.RetrieveAPIView):
    """Get a specific book"""

    queryset = Book.objects
    serializer_class = BookSerializer


class GenresList(generics.ListAPIView):
    """Get all genres"""

    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer