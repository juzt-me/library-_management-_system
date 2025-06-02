from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('FICTION', 'Fiction'),
        ('NON_FICTION', 'Non-Fiction'),
        ('SCIENCE', 'Science'),
        ('TECHNOLOGY', 'Technology'),
        ('HISTORY', 'History'),
        ('LITERATURE', 'Literature'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def is_available(self):
        return self.available_quantity > 0

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    membership_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"

    def get_borrowed_books(self):
        return BookLending.objects.filter(member=self, returned_date__isnull=True)

    def has_overdue_books(self):
        return self.get_borrowed_books().filter(due_date__lt=timezone.now()).exists()

class BookLending(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.book.title} - {self.member.user.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.pk:  # If this is a new lending
            self.due_date = timezone.now() + timedelta(days=14)  # 2 weeks lending period
            self.book.available_quantity -= 1
            self.book.save()
        super().save(*args, **kwargs)

    def return_book(self):
        if not self.returned_date:
            self.returned_date = timezone.now()
            self.calculate_fine()
            self.book.available_quantity += 1
            self.book.save()
            self.save()

    def calculate_fine(self):
        if self.returned_date and self.returned_date > self.due_date:
            days_overdue = (self.returned_date - self.due_date).days
            self.fine_amount = days_overdue * 1.00  # $1 per day
            self.save()

    def is_overdue(self):
        return not self.returned_date and timezone.now() > self.due_date
