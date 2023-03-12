from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q, Max
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views.decorators.cache import cache_page

from proreader.settings import MEDIA_ROOT
from web.forms import RegistrationForm, AuthorizationForm, BookNoteForm, BookTagForm, FavouriteGenreForm, \
    BookNoteFilterForm, ImportForm
from web.models import Book, BookTag, FavouriteGenre
from web.services import filter_book_notes, export_book_notes_as_csv, import_book_notes_from_csv, get_stat

User = get_user_model()


@cache_page(10)
@login_required
def main_view(request):
    book_notes = Book.objects.filter(user=request.user).order_by('title')
    current_book = book_notes.filter(done=False).first()

    filter_form = BookNoteFilterForm(request.GET)
    filter_form.is_valid()
    book_notes = filter_book_notes(book_notes, filter_form.cleaned_data)

    total_count = book_notes.count()
    book_notes = book_notes.prefetch_related('tags').select_related('user').annotate(
        tags_count=Count('tags')
    )

    page_number = request.GET.get('page', 1)
    paginator = Paginator(book_notes, per_page=600)

    if request.GET.get('export') == 'csv':
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=book_notes.csv'}
        )
        return export_book_notes_as_csv(book_notes, response)

    return render(request, 'web/main.html', {
        'book_notes': paginator.get_page(page_number),
        'MEDIA_ROOT': MEDIA_ROOT,
        'current_book': current_book,
        'total_count': total_count,
        'form': BookNoteForm(),
        'filter_form': filter_form
    })


@login_required
def import_view(request):
    if request.method == 'POST':
        form = ImportForm(files=request.FILES)
        if form.is_valid():
            import_book_notes_from_csv(form.cleaned_data['file'], request.user.id)
            return redirect('main')
    return render(request, 'web/import.html', {
        'form': ImportForm()
    })


@login_required
def stat_view(request):
    return render(request, 'web/stat.html', {'results': get_stat()})


@login_required
def analytics_view(request):
    overall_stat = Book.objects.filter(user=request.user).aggregate(count=Count('id'))
    genre_stat = (
        Book.objects
        .values('genre')
        .annotate(
            count=Count('id'),
            is_done_count=Count('id', filter=Q(done=True))
        )
    )
    max_popular_genre = genre_stat.aggregate(max_count=Max('count'))
    max_popular_genre = genre_stat.filter(count=max_popular_genre['max_count'])[0]
    return render(request, 'web/analytics.html', {
        'overall_stat': overall_stat,
        'genre_stat': genre_stat,
        'max_popular_genre': max_popular_genre
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


@login_required
def logout_view(request):
    logout(request)
    return redirect('main')


@login_required
def book_add_view(request):
    form = BookNoteForm()
    if request.method == 'POST':
        form = BookNoteForm(data=request.POST, files=request.FILES,  initial={'user': request.user})
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request, 'web/book_note_form.html', {'form': form})


@login_required
def book_edit_view(request, id=None):
    book_note = get_object_or_404(Book, user=request.user, id=id) if id is not None else None
    form = BookNoteForm(instance=book_note)
    if request.method == 'POST':
        form = BookNoteForm(data=request.POST, files=request.FILES,
                            instance=book_note, initial={'user': request.user})
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request, 'web/book_note_form.html', {'form': form})


@login_required
def book_delete_view(request, id):
    book_note = get_object_or_404(Book, user=request.user, id=id)
    book_note.delete()
    return redirect('main')


@login_required
def book_check_view(request, id):
    if request.method == 'POST':
        book = get_object_or_404(Book, user=request.user, id=id)
        book.done = True
        book.save()
    return redirect('main')


@login_required
def _list_editor_view(request, model_cls, form_cls, template_name, url_name):
    items = model_cls.objects.filter(user=request.user).order_by('title')
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


@login_required
def tags_view(request):
    return _list_editor_view(request, BookTag, BookTagForm, 'tags', 'tags')


@login_required
def tags_delete_view(request, id):
    tag = get_object_or_404(BookTag, user=request.user, id=id)
    tag.delete()
    return redirect('tags')


@login_required
def genres_view(request):
    return _list_editor_view(request, FavouriteGenre, FavouriteGenreForm, 'genres', 'genres')


@login_required
def genres_delete_view(request, id):
    genre = get_object_or_404(FavouriteGenre, user=request.user, id=id)
    genre.delete()
    return redirect('genres')
