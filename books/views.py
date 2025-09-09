from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from books.permissions import IsLibrarianOrReadOnly
from .models import BorrowRecord, Review, Book, Waitlist
from .serializers import (
    BookSerializer,
    BorrowRecordSerializer,
    ReviewSerializer,
    WaitlistSerializer,
)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsLibrarianOrReadOnly]
    serializer_class = BookSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'author', 'isbn', 'category']
    filterset_fields = ['category']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def borrow(self, request, pk=None):
        book = self.get_object()

        # Check availability
        if book.copies <= 0:
            return Response(
                {"detail": "No copies available. You have been added to the waitlist."},
                status=status.HTTP_400_BAD_REQUEST
            )


        borrow = BorrowRecord.objects.create(
            user=request.user,
            book=book,
            due_date=timezone.now() + timezone.timedelta(minutes=2)
        )


        book.copies -= 1
        book.save()

        return Response(BorrowRecordSerializer(borrow).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def return_book(self, request, pk=None):
        book = self.get_object()

        borrow = BorrowRecord.objects.filter(
            book=book, user=request.user, returned=False
        ).first()

        if not borrow:
            return Response({"detail": "No active borrow record found."}, status=404)


        borrow.returned = True
        borrow.return_date = timezone.now()


        if borrow.return_date > borrow.due_date:
            delta = borrow.return_date - borrow.due_date
            minutes_overdue = int(delta.total_seconds() / 60)
            borrow.fine = minutes_overdue * 10
        else:
            borrow.fine = 0

        borrow.save()


        book.copies += 1
        book.save()

        # ✅ waitlist handle (give to next user for 2 minutes)
        next_user = Waitlist.objects.filter(book=book).order_by('created_at').first()
        if next_user:
            BorrowRecord.objects.create(
                user=next_user.user,
                book=book,
                due_date=timezone.now() + timezone.timedelta(minutes=2)
            )
            next_user.delete()

        return Response({
            "detail": "Book returned successfully.",
            "fine": str(borrow.fine)
        })


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




