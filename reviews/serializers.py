from rest_framework import serializers
from .models import Review, ReviewLike

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'book_title', 'rating', 'comment', 'created_at']


class ReviewLikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    review_id = serializers.IntegerField(source='review.id', read_only=True)

    class Meta:
        model = ReviewLike
        fields = ['id', 'user', 'review_id', 'vote_type']