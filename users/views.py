from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model
from users.permissions import IsAdmin

User = get_user_model()
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]