from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.serializers import BookNoteSerializer, TagSerializer
from web.models import Book, BookTag


@api_view(['GET'])
@permission_classes([])
def main_view(request):
    return Response({'status': 'ok'})


class BookNotesViewSet(ModelViewSet):
    serializer_class = BookNoteSerializer

    def get_queryset(self):
        return Book.objects.all().select_related('user').prefetch_related('tags').filter(user=self.request.user)


class BookTagsViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        return BookTag.objects.all().filter(user=self.request.user)

