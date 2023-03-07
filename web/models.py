from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class BookTag(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    author = models.CharField(max_length=40, default="Indefined", verbose_name='Автор')
    genre = models.CharField(max_length=20, verbose_name='Жанр')
    description = models.CharField(max_length=500, default="--", verbose_name='Описание')
    done = models.BooleanField(default=False, verbose_name='Стадия прочтения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    tags = models.ManyToManyField(BookTag, verbose_name='Теги')
    image = models.ImageField(upload_to="books/", null=True, blank=True, verbose_name='Картинка')


class FavouriteGenre(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
