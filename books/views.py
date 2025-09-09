from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from books.permissions import IsLibrarianOrReadOnly
from .models import BorrowRecord, Book, Waitlist
from .serializers import (BookSerializer, BorrowRecordSerializer, WaitlistSerializer)

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
        user = request.user


        if book.copies <= 0:
            return Response(
                {"detail": "No copies available. You have been added to the waitlist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if BorrowRecord.objects.filter(user=user, book=book, returned=False).exists():
            return Response(
                {"detail": "You have already borrowed this book."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Create borrow record
        borrow = BorrowRecord.objects.create(
            user=user,
            book=book,
            due_date=timezone.now() + timezone.timedelta(minutes=2)
        )

        # Decrease available copies
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
            minutes_overdue = int(delta.total_seconds() / 8)
            borrow.fine = minutes_overdue * 10
        else:
            borrow.fine = 0
        borrow.save()
        book.copies += 1
        book.save()

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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join_waitlist(self, request, pk=None):
        book = self.get_object()

        if book.copies > 0:
            return Response({"detail": "Book is available, no need to join waitlist."}, status=400)

        waitlist, created = Waitlist.objects.get_or_create(user=request.user, book=book)

        if not created:
            return Response({"detail": "Already in waitlist."}, status=400)

        return Response(WaitlistSerializer(waitlist).data, status=201)








