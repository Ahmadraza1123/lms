from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Review, ReviewLike
from books.models import BorrowRecord
from .serializers import ReviewSerializer, ReviewLikeSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        user = self.request.user

        if not BorrowRecord.objects.filter(user=user, book=book).exists():
            raise ValidationError({"detail": "You must borrow this book before reviewing."})

        if Review.objects.filter(user=user, book=book).exists():
            raise ValidationError({"detail": "You have already reviewed this book."})

        serializer.save(user=user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        review = self.get_object()
        like_instance, _ = ReviewLike.objects.update_or_create(
            user=request.user,
            review=review,
            defaults={'vote_type': 'like'}
        )
        serializer = ReviewLikeSerializer(like_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        review = self.get_object()
        like_instance, _ = ReviewLike.objects.update_or_create(
            user=request.user,
            review=review,
            defaults={'vote_type': 'dislike'}
        )
        serializer = ReviewLikeSerializer(like_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewLikeViewSet(viewsets.ModelViewSet):
    queryset = ReviewLike.objects.all()
    serializer_class = ReviewLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return ReviewLike.objects.filter(user=self.request.user)
