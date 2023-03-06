from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, book_add_view

urlpatterns = [
    path('', main_view, name='main'),
    path('registration/', registration_view, name='registration'),
    path('auth/', auth_view, name='authorization'),
    path('logout/', logout_view, name='logout'),
    path('book_notes/add/', book_add_view, name='book_add')
]
