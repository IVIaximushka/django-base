from django import forms
from django.contrib.auth import get_user_model

from web.models import Book, BookTag, FavouriteGenre

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error('password', 'Пароли не совпадают!')
        return cleaned_data

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')


class AuthorizationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class BookNoteForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = Book
        fields = ('title', 'author', 'genre', 'description', 'done', 'image', 'tags')


class BookTagForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = BookTag
        fields = ('title',)


class FavouriteGenreForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = FavouriteGenre
        fields = ('title',)


class BookNoteFilterForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Поиск'}), required=False)
    is_done = forms.NullBooleanField(
        widget=forms.Select(
            choices=(
                ('unknown', 'Процесс прочтения'),
                ('true', 'Прочитано'),
                ('false', 'Не прочитано')
            )
        )
    )
    genres = forms.ChoiceField(
        choices=(
            ('', 'Любой жанр'),
            ('фэнтези', 'фэнтези'),
            ('вестерн', 'вестерн'),
            ('драма', 'драма'),
            ('реализм', 'реализм'),
            ('классика', 'классика'),
            ('романтизм', 'романтизм')
        ), required=False
    )
