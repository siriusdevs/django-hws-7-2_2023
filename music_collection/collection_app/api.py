from .models import Tracks, Albums, Genres, Client, Artists
from rest_framework import viewsets, permissions
from .serializers import *

class TrackViewSet(viewsets.ModelViewSet):
    query_set = Tracks.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TrackSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    query_set = Albums.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AlbumSerializer

class ArtistViewSet(viewsets.ModelViewSet):
    query_set = Artists.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ArtistSerializer

class GenreViewSet(viewsets.ModelViewSet):
    query_set = Tracks.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = GenreSerializer

class ClientViewSet(viewsets.ModelViewSet):
    query_set = Tracks.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ClientSerializer