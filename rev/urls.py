from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, ReviewViewSet, UserViewSet, CartViewSet  

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'users', UserViewSet)
router.register(r'cart', CartViewSet, basename='cart') 

urlpatterns = router.urls
