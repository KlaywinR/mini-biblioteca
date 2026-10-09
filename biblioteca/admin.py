from django.contrib import admin
from .models import Author, Book, Category

class BookInline(admin.TabularInline):
    model = Book
    extra = 1

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "nationality")
    search_fields = ("name",)
    inlines = [BookInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year_of_publication", "available")
    search_fields = ("title", "author__name")
    list_filter = ("available", "categories")
    filter_horizontal = ("categories",)
