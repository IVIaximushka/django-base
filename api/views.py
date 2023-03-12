from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import BookNoteSerializer
from web.models import Book


@api_view(['GET'])
@permission_classes([])
def main_view(request):
    return Response({'status': 'ok'})


class BookNotesViewSet(ModelViewSet):
    serializer_class = BookNoteSerializer

    def get_queryset(self):
        return Book.objects.all().select_related('user').prefetch_related('tags').filter(user=self.request.user)
