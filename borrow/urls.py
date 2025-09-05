from rest_framework.routers import DefaultRouter
from .views import BorrowViewSet, WaitlistViewSet

router = DefaultRouter()
router.register(r'borrows', BorrowViewSet, basename='borrow')
router.register(r'waitlist', WaitlistViewSet, basename='waitlist')

urlpatterns = router.urls
