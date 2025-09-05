from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)



class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.available_copies > self.copies:
            self.available_copies = self.copies
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.available_copies}/{self.copies})"
def default_due_date():
    return timezone.now() + timedelta(days=14)


class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=default_due_date)
    returned = models.BooleanField(default=False)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField(blank=True)
