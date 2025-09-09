from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'detail', BookViewSet)
router.register(r'reviews', ReviewViewSet)
# router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
