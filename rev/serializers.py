from rest_framework import serializers
from .models import Service, Review, Cart
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'service', 'rating', 'comment', 'created_at', 'user']

    def validate(self, data):
        user = self.context['request'].user
        service = data.get('service')

        if Review.objects.filter(user=user, service=service).exists():
            raise serializers.ValidationError("You have already reviewed this service.")
        return data


class ServiceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'created_at', 'user', 'reviews']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    service_name = serializers.ReadOnlyField(source='service.name')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'service', 'service_name', 'added_at']
