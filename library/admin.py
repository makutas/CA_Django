from django.contrib import admin
from .models import *


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'display_books')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'display_genre')
    search_fields = ('title', )


class BookInstanceAdmin(admin.ModelAdmin):
    # def available_on(self, obj):
    #     return obj.due_back.strftime('%Y-%m-%d')

    list_display = ('book', 'book_status', 'due_back')

    list_filter = ('book_status', 'due_back')
    fieldsets = (
        ('General', {'fields': ('instance_id', 'book')}),
        ('Availability', {'fields': ('book_status', 'due_back')}),
    )
    search_fields = ('instance_id', 'book__title')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
