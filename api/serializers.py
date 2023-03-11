from rest_framework import serializers

from web.models import User, BookTag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTag
        fields = ('id', 'title')


class BookNoteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    author = serializers.CharField()
    genre = serializers.CharField()
    description = serializers.CharField()
    done = serializers.BooleanField()
    user = UserSerializer()
    tags = TagSerializer(many=True)
