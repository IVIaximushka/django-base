import csv

from web.models import Book, BookTag


def filter_book_notes(book_note_qs, filter: dict):
    if filter['search']:
        book_note_qs = book_note_qs.filter(title__icontains=filter['search'])

    if filter['is_done'] is not None:
        book_note_qs = book_note_qs.filter(done=filter['is_done'])

    if filter['genres']:
        book_note_qs = book_note_qs.filter(genre=filter['genres'])
    return book_note_qs


def export_book_notes_as_csv(book_notes, response):
    writer = csv.writer(response)
    writer.writerow(('title', 'author', 'genre', 'description', 'done', 'tags'))

    for book_note in book_notes:
        writer.writerow((book_note.title, book_note.author, book_note.genre, book_note.description,
                         book_note.done, ' '.join([tag.title for tag in book_note.tags.all()])))
    return response


def import_book_notes_from_csv(file, user_id):
    strs_from_file = [row.decode() for row in file]
    reader = csv.DictReader(strs_from_file)

    book_notes = []
    book_note_tags = []
    for row in reader:
        book_notes.append(Book(
            title=row['title'],
            author=row['author'],
            genre=row['genre'],
            description=row['description'],
            done=row['done'],
            user_id=user_id
        ))
        book_note_tags.append(row['tags'].split() if row['tags'] else [])

    tags_map = dict(BookTag.objects.all().values_list('title', 'id'))
    saved_book_notes = Book.objects.bulk_create(book_notes)
    booknote_tags = []
    for book, book_note_tags_item in zip(saved_book_notes, book_note_tags):
        for tag in book_note_tags_item:
            booknote_tags.append(
                Book.tags.through(book_id=book.id, booktag_id=tags_map[tag])
            )
    Book.tags.through.objects.bulk_create(booknote_tags)
