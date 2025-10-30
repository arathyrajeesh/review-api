from rest_framework import serializers
from .models import Service, Review
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


class ServiceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'created_at', 'user', 'reviews']
