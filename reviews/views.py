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
            defaults={'vote': 'like'}
        )
        serializer = ReviewLikeSerializer(like_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        review = self.get_object()
        like_instance, _ = ReviewLike.objects.update_or_create(
            user=request.user,
            review=review,
            defaults={'vote': 'dislike'}
        )
        serializer = ReviewLikeSerializer(like_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewLikeViewSet(viewsets.ModelViewSet):
    queryset = ReviewLike.objects.all()
    serializer_class = ReviewLikeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        review = self.get_object()
        user = request.user
        vote_type = request.data.get('vote')  # 'like' or 'dislike'

        if vote_type not in ['like', 'dislike']:
            return Response({'detail': 'Invalid vote type'}, status=status.HTTP_400_BAD_REQUEST)

        obj, created = ReviewLike.objects.update_or_create(
            user=user,
            review=review,
            defaults={'vote_type': vote_type}
        )

        serializer = ReviewLikeSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
