#Register your models here.
from django.contrib import admin
from django.db.models import Count
from .models import Artists, Albums, Tracks, Genres, Client, \
TrackGenre, AlbumGenre, TrackAlbum, ArtistAlbum, TrackClient
from datetime import datetime

# curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'


class TrackGenreInline(admin.TabularInline):
    model = TrackGenre
    extra = 1

class AlbumGenreInline(admin.TabularInline):
    model = AlbumGenre
    extra = 1

class TrackAlbumInline(admin.TabularInline):
    model = TrackAlbum
    extra = 1

class ArtistAlbumInline(admin.TabularInline):
    model = ArtistAlbum
    extra = 1

class TrackClientInline(admin.TabularInline):
    model = TrackClient
    extra = 1

class TrackInline(admin.TabularInline):
    model = Tracks
    extra = 1


@admin.register(Tracks)
class TrackAdmin(admin.ModelAdmin):
    model = Tracks
    inlines = (TrackClientInline, TrackGenreInline, TrackAlbumInline)
    list_display = ('title', 'audio_file', 'duration', 'year', 'country', 'rating')
    list_filter = (
        'genres',
        'duration',
        'rating',
    )

@admin.register(Artists)
class ArtistAdmin(admin.ModelAdmin):
    model = Artists
    inlines = [TrackAlbumInline,]
    list_display = ('name', 'birth_date', 'country', 'education')
    list_filter = (
        'tracks', 
        'country', 
        'education', 
    )

@admin.register(Albums)
class AlbumAdmin(admin.ModelAdmin):
    model = Albums
    inlines = [ArtistAlbumInline,]

    def get_queryset(self, request):            #аннотация `num_tracks` к альбому
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(num_tracks=Count('tracks'))
        return queryset

    def num_tracks(self, obj):                  #отображение количества треков в каждом альбоме
        return obj.num_tracks

    num_tracks.admin_order_field = 'num_tracks' #сортировка по количеству треков


@admin.register(Genres)
class GenreAdmin(admin.ModelAdmin):
    model = Genres
    inlines = (TrackGenreInline,AlbumGenreInline,)
    list_filter = (
        'tracks',
        'albums',
        )

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = (TrackClientInline,)