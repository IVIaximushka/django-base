from django.contrib import admin

from web.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre', 'description', 'done', 'user')
    search_fields = ('id', 'title')
    list_filter = ('author', 'genre', 'done')
    ordering = ('title',)
    readonly_fields = ('done',)


admin.site.register(Book, BookAdmin)
