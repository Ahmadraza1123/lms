from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, ReviewLikeViewSet

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'review-likes', ReviewLikeViewSet, basename='reviewlike')

urlpatterns = [
    path('', include(router.urls)),
]
