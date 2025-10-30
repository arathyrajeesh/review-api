from rest_framework import viewsets, permissions, serializers,status
from .models import Service, Review, Cart
from .serializers import ServiceSerializer, ReviewSerializer, UserSerializer, CartSerializer
from django.contrib.auth.models import User
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        service = serializer.validated_data['service']
        user = self.request.user
        if Cart.objects.filter(user=user, service=service).exists():
            raise serializers.ValidationError({'detail': 'Service already in cart'})
        serializer.save(user=user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        total_items = cart_items.count()
        total_services = [item.service.name for item in cart_items]
        return Response({
            'user': request.user.username,
            'total_items': total_items,
            'services': total_services
        })

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        deleted_count, _ = Cart.objects.filter(user=request.user).delete()
        return Response(
            {'message': f'{deleted_count} items removed from your cart.'},
            status=status.HTTP_200_OK
        )
