from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, ReviewLikeViewSet

router = DefaultRouter()
router.register('reviews', ReviewViewSet, basename='reviews')
router.register('review-likes', ReviewLikeViewSet, basename='review-likes')

urlpatterns = router.urls
