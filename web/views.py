from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout

from web.forms import RegistrationForm, AuthorizationForm, BookNoteForm, BookTagForm, FavouriteGenreForm
from web.models import Book, BookTag, FavouriteGenre

User = get_user_model()


def main_view(request):
    book_notes = Book.objects.all()
    return render(request, 'web/main.html', {
        'book_notes': book_notes
    })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, 'web/registration.html', {
        'form': form,
        'is_success': is_success
    })


def auth_view(request):
    form = AuthorizationForm()
    if request.method == 'POST':
        form = AuthorizationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, 'Введены неверные данные')
            else:
                login(request, user)
                return redirect('main')
    return render(request, 'web/auth.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main')


def book_add_view(request):
    form = BookNoteForm()
    if request.method == 'POST':
        form = BookNoteForm(data=request.POST, files=request.FILES,  initial={'user': request.user})
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request, 'web/book_note_form.html', {'form': form})


def book_edit_view(request, id=None):
    book_note = Book.objects.get(id=id) if id is not None else None
    form = BookNoteForm(instance=book_note)
    if request.method == 'POST':
        form = BookNoteForm(data=request.POST, files=request.FILES,
                            instance=book_note, initial={'user': request.user})
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request, 'web/book_note_form.html', {'form': form})


def _list_editor_view(request, model_cls, form_cls, template_name, url_name):
    items = model_cls.objects.all()
    form = form_cls()
    if request.method == 'POST':
        form = form_cls(data=request.POST, initial={'user': request.user})
        if form.is_valid():
            form.save()
            return redirect(f'{url_name}')
    return render(request, f'web/{template_name}.html', {
        'items': items,
        'form': form
    })


def tags_view(request):
    return _list_editor_view(request, BookTag, BookTagForm, 'tags', 'tags')


def tags_delete_view(request, id):
    tag = BookTag.objects.get(id=id)
    tag.delete()
    return redirect('tags')


def genres_view(request):
    return _list_editor_view(request, FavouriteGenre, FavouriteGenreForm, 'genres', 'genres')


def genres_delete_view(request, id):
    genre = FavouriteGenre.objects.get(id=id)
    genre.delete()
    return redirect('genres')
