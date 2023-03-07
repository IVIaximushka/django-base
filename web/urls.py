from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, book_add_view, book_edit_view, tags_view, \
    tags_delete_view

urlpatterns = [
    path('', main_view, name='main'),
    path('registration/', registration_view, name='registration'),
    path('auth/', auth_view, name='authorization'),
    path('logout/', logout_view, name='logout'),
    path('book_notes/add/', book_add_view, name='book_add'),
    path('book_notes/<int:id>/', book_edit_view, name='book_edit'),
    path('tags/', tags_view, name='tags'),
    path('tags/<int:id>/delete/', tags_delete_view, name='tags_delete')
]
