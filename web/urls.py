from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, book_add_view, book_edit_view, tags_view, \
    tags_delete_view, genres_delete_view, genres_view, book_delete_view, book_check_view, analytics_view, import_view

urlpatterns = [
    path('', main_view, name='main'),
    path('registration/', registration_view, name='registration'),
    path('auth/', auth_view, name='authorization'),
    path('logout/', logout_view, name='logout'),
    path('book_notes/add/', book_add_view, name='book_add'),
    path('book_notes/<int:id>/', book_edit_view, name='book_edit'),
    path('book_notes/<int:id>/delete', book_delete_view, name='book_delete'),
    path('book_notes/<int:id>/check', book_check_view, name='book_check'),
    path('tags/', tags_view, name='tags'),
    path('tags/<int:id>/delete/', tags_delete_view, name='tags_delete'),
    path('genres/', genres_view, name='genres'),
    path('genres/<int:id>/delete/', genres_delete_view, name='genres_delete'),
    path('analytics/', analytics_view, name='analytics'),
    path('import/', import_view, name='import'),
]
