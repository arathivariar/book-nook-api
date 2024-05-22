from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from booknook_api.permissions import IsOwnerOrReadOnly
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListCreateAPIView):
    """
    List books or create a book if logged in
    The perform_create method associates the book with the logged in user.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Book.objects.annotate(
        likes_count=Count('likes', distinct=True),
        #comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
        'author',
    ]
    ordering_fields = [
        'likes_count',
        #'comments_count',
        'likes__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a book and edit or delete it if you own it.
    """
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Book.objects.annotate(
        likes_count=Count('likes', distinct=True),
        #comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')