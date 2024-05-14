from rest_framework import generics, permissions
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
    queryset = Book.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a book and edit or delete it if you own it.
    """
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Book.objects.all()