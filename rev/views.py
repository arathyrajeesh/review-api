from rest_framework import viewsets, permissions
from .models import Service, Review
from .serializers import ServiceSerializer, ReviewSerializer, UserSerializer
from django.contrib.auth.models import User
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly


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
