def filter_book_notes(book_note_qs, filter: dict):
    if filter['search']:
        book_note_qs = book_note_qs.filter(title__icontains=filter['search'])

    if filter['is_done'] is not None:
        book_note_qs = book_note_qs.filter(done=filter['is_done'])

    if filter['genres']:
        book_note_qs = book_note_qs.filter(genre=filter['genres'])
    return book_note_qs
