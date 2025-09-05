from rest_framework import viewsets, permissions
from .models import Borrow, Waitlist
from .serializers import BorrowSerializer, WaitlistSerializer


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WaitlistViewSet(viewsets.ModelViewSet):
    queryset = Waitlist.objects.all()
    serializer_class = WaitlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
