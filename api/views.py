from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import BookNoteSerializer
from web.models import Book


@api_view(['GET'])
def main_view(request):
    return Response({'status': 'ok'})


@api_view(['GET'])
def book_notes_view(request):
    book_notes = Book.objects.all().select_related('user').prefetch_related('tags')
    serializer = BookNoteSerializer(book_notes, many=True)
    return Response(serializer.data)
