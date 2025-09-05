from django.db import models
from django.utils import timezone
from django.conf import settings
from books.models import Book
from datetime import timedelta

User = settings.AUTH_USER_MODEL


def default_due_date():
    return timezone.now() + timedelta(days=14)


class Borrow(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('late', 'Late'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrows")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=default_due_date)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="borrowed")
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def mark_returned(self):
        self.return_date = timezone.now()
        if self.return_date > self.due_date:
            self.status = 'late'
            days_overdue = (self.return_date - self.due_date).days
            self.fine = days_overdue * 10  # replace with settings.FINE_RATE if needed
        else:
            self.status = 'returned'
        self.book.available_copies += 1
        self.book.save()
        self.save()

    def __str__(self):
        return f"{self.user} → {self.book} ({self.status})"


class Waitlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="waitlists")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="waitlists")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} waiting for {self.book}"
