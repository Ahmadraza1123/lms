from rest_framework import serializers
from .models import Review, ReviewLike

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'comment', 'created_at']


class ReviewLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ReviewLike
        fields = ['id', 'user', 'review', 'is_like']
