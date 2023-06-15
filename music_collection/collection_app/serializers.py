from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Tracks, Artists, Genres, Albums, Client
###############################################

class ClientSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'account_name', 'money', 'users', 'created']

class TrackSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Tracks
        fields = ('id', 'title', 'audio_file', 'duration', 'year', 'country', 'rating', 'created', 'modified')


class ArtistSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Artists
        fields = ('id', 'name', 'birth_date', 'country', 'education')


class GenreSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Genres
        fields = ('id', 'title', 'description')

class AlbumSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Albums
        fields = ('id', 'title', 'year', 'category')
