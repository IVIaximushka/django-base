from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class BookTag(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=40, default="Indefined")
    genre = models.CharField(max_length=20)
    description = models.CharField(max_length=500, default="--")
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(BookTag)
    image = models.ImageField(upload_to="books/", null=True, blank=True)


class FavouriteGenre(models.Model):
    title = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
