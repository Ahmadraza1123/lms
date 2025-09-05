from rest_framework import viewsets, permissions
from .models import Review, ReviewLike
from .serializers import ReviewSerializer, ReviewLikeSerializer
from users.permissions import IsMember

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsMember()]


class ReviewLikeViewSet(viewsets.ModelViewSet):
    queryset = ReviewLike.objects.all()
    serializer_class = ReviewLikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
