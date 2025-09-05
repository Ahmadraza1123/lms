from rest_framework import viewsets, status,filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Category, BorrowRecord, Review
from .serializers import BookSerializer, CategorySerializer, BorrowRecordSerializer, ReviewSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'author', 'isbn', 'category__name']
    filterset_fields = ['category__name', 'available_copies']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def borrow(self, request, pk=None):
        book = self.get_object()
        if book.available_copies <= 0:
            return Response({"detail": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)
        borrow = BorrowRecord.objects.create(user=request.user, book=book, due_date=timezone.now() + timezone.timedelta(days=14))
        book.available_copies -= 1
        book.save()
        return Response(BorrowRecordSerializer(borrow).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def return_book(self, request, pk=None):
        book = self.get_object()
        borrow = get_object_or_404(BorrowRecord, book=book, user=request.user, returned=False)
        borrow.returned = True
        borrow.save()
        book.available_copies += 1
        book.save()
        return Response({"detail": "Book returned"})

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
