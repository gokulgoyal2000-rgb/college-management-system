from django.contrib import admin
from .models import Book, BookIssue

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'total_copies', 'available_copies', 'category']
    search_fields = ['title', 'author', 'isbn']
    list_filter = ['category', 'publication_year']

@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'member_type', 'issue_date', 'due_date', 'is_returned', 'fine_amount']
    list_filter = ['member_type', 'is_returned', 'issue_date']
    search_fields = ['book__title']
    date_hierarchy = 'issue_date'