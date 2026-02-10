from django.contrib import admin
from .models import User, Author, Genre, Book, BorrowRequest, BookReview

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "is_staff")
    list_filter = ("role", "is_staff")
    search_fields = ("username", "email")

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "ISBN", "available_copies", "total_copies")
    list_filter = ("author", "genres")
    search_fields = ("title", "ISBN")
    filter_horizontal = ("genres",)

@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "user", "status", "requested_at", "approved_at", "returned_at")
    list_filter = ("status", "requested_at", "approved_at", "returned_at")
    search_fields = ("book__title", "user__username")

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("book__title", "user__username")
