import random

from django.core.management.base import BaseCommand

from web.models import User, Book, BookTag


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.filter(id=1).first()
        tags = BookTag.objects.filter(user=user)
        new_books = []
        for book_index in range(30):
            new_books.append(Book(
                title=f'generated book {book_index}',
                author=random.choice(['Оруэлл',
                                      'Пушкин',
                                      'Симмонс',
                                      'Толкин',
                                      'Сапковский',
                                      'Толстой',
                                      'Достоевский',
                                      'Гёте']),
                genre=random.choice(['фэнтези',
                                     'вестерн',
                                     'драма',
                                     'реализм',
                                     'классика',
                                     'романтизм']),
                done=random.choice([True, False]),
                user=user
            ))

        saved_books = Book.objects.bulk_create(new_books)
        book_tags = []
        for book in saved_books:
            count_of_tags = random.randint(0, len(tags))
            for tag_index in range(count_of_tags):
                book_tags.append(
                    Book.tags.through(book_id=book.id, booktag_id=tags[tag_index].id)
                )
        Book.tags.through.objects.bulk_create(book_tags)
