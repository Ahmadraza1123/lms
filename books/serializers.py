from rest_framework import serializers
from .models import Book, BorrowRecord, Waitlist


class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'description', 'copies', 'categories','average_rating']

    def get_average_rating(self, obj):
        return obj.average_rating()


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = '__all__'


class WaitlistSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Waitlist
        fields = ['id', 'created_at', 'user', 'user_name', 'book', 'book_title']