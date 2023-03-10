import csv


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
