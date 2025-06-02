from django.contrib import admin
from .models import Book, Member, BookLending

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'quantity', 'available_quantity')
    list_filter = ('category',)
    search_fields = ('title', 'author', 'isbn')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'membership_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'user__email', 'phone_number')

@admin.register(BookLending)
class BookLendingAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'issue_date', 'due_date', 'returned_date', 'fine_amount')
    list_filter = ('returned_date',)
    search_fields = ('book__title', 'member__user__username')
