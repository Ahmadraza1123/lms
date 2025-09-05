from rest_framework import serializers
from .models import Book, Category, BorrowRecord, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = '__all__'
        read_only_fields = ['user', 'borrow_date']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']
