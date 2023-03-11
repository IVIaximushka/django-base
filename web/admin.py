from django.contrib import admin

from web.models import Book, BookTag


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre', 'description', 'done', 'user')
    search_fields = ('id', 'title')
    list_filter = ('author', 'genre', 'done', 'user')
    ordering = ('title',)
    readonly_fields = ('done',)


class BookTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user')
    search_fields = ('id', 'title')
    list_filter = ('user',)
    ordering = ('title',)


admin.site.register(Book, BookAdmin)
admin.site.register(BookTag, BookTagAdmin)
