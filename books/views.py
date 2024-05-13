from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book
from .serializers import BookSerializer
from booknook_api.permissions import IsOwnerOrReadOnly


class BookList(APIView):
    serializer_class = BookSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(
            books, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class BookDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = BookSerializer

    def get_object(self, pk):
        try:
            book = Book.objects.get(pk=pk)
            self.check_object_permissions(self.request, book)
            return book
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(
            book, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(
            book, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )