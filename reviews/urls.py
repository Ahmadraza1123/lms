from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, ReviewLikeViewSet

router = DefaultRouter()
router.register(r'comment', ReviewViewSet, basename='comment')
router.register(r'vote', ReviewLikeViewSet, basename='vote')

urlpatterns = [
    path('', include(router.urls)),
]
