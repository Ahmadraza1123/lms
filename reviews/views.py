from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Review, ReviewLike
from books.models import BorrowRecord
from .serializers import ReviewSerializer, ReviewLikeSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        user = self.request.user


        if not BorrowRecord.objects.filter(user=user, book=book).exists():
            raise ValidationError({"detail": "You must borrow this book before reviewing."})

        serializer.save(user=user)

    def get_permissions(self):
        return [permissions.IsAuthenticated()]


class ReviewLikeViewSet(viewsets.ModelViewSet):
    queryset = ReviewLike.objects.all()
    serializer_class = ReviewLikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
