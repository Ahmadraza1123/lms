from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CategoryViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
