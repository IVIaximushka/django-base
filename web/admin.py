from django.contrib import admin

from web.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'description', 'done')


admin.site.register(Book, BookAdmin)
