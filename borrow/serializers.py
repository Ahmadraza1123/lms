from rest_framework import serializers
from .models import Borrow, Waitlist


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = '__all__'
        read_only_fields = ['user', 'borrow_date', 'due_date', 'return_date', 'status', 'fine']

    def create(self, validated_data):
        user = self.context['request'].user
        book = validated_data['book']

        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()
            borrow = Borrow.objects.create(user=user, **validated_data)
            return borrow
        else:
            raise serializers.ValidationError("No copies available. Please join waitlist.")


class WaitlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = '__all__'
        read_only_fields = ['user', 'book', 'created_at']
