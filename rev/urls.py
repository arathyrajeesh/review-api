from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, ReviewViewSet

router = DefaultRouter()
router.register('services', ServiceViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = router.urls
