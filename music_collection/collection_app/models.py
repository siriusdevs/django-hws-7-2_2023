# Модели определяют поля в бд - структурные элементы таблицы, которые определяют типы данных, которые могут быть хранены в таблице. Каждое поле представляет собой отдельное свойство или атрибут записи в таблице.

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import  MinValueValidator, MaxValueValidator
from uuid import uuid4
from datetime import datetime
from . import config
from django.utils.translation import gettext_lazy as _
from django.conf.global_settings import AUTH_USER_MODEL
from mutagen.mp3 import MP3
from django.conf import settings

# settings.configure( 
#     ROOT_URLCONF=__name__,
# )

# Create your models here.

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    class Meta:
        abstract = True

class CreatedMixin(models.Model):
    created = models.DateTimeField(_('created'), default=datetime.now, blank=True, null=False)

    class Meta:
        abstract = True

class ModifiedMixin(models.Model):
    modified = models.DateTimeField(_('modified'), default=datetime.now, blank=True, null=False)

    class Meta:
        abstract = True

# Основные таблицы

class Tracks(UUIDMixin, CreatedMixin, ModifiedMixin):
    album = models.ForeignKey('Albums', on_delete=models.CASCADE, blank=True, null=True)  
    title = models.CharField(max_length=50)
    audio_file = models.FileField(upload_to='static/audio_files/', null=False, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2023)])    
    country = models.TextField(blank=True)
    rating = models.IntegerField()

    def clean(self):
        if self.audio_file:
            audio = MP3(self.audio_file.path)
            duration = int(audio.info.length)
            if duration > 300: # 5 минут
                raise ValidationError(_('Продолжительность трека не может превышать 5 минут.'))
            self.duration = duration

    @property
    def get_audio_url(self):
        if self.audio_file and hasattr(self.audio_file, 'url'):
            return self.audio_file.url
        else:
            return "/static/audio_files/I_Had_a_Feeling _-_ TrackTribe.mp3"

    def __str__(self):
        return f'{self.title}, {self.country}, {self.duration}'

    class Meta:
        db_table = '"collection"."tracks"'
        verbose_name = _('track')
        verbose_name_plural = _('tracks')

class Artists(UUIDMixin, CreatedMixin, ModifiedMixin):
    tracks = models.ManyToManyField(Tracks, blank=True)
    name = models.CharField(max_length=50)
    birth_date = models.DateField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    education = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.name}' 

    class Meta:
        db_table = '"collection"."artists"'
        verbose_name = _('artist')
        verbose_name_plural = _('artists')

class Albums(UUIDMixin, CreatedMixin, ModifiedMixin):
    artist = models.ManyToManyField(Artists, blank=True)
    genres = models.ManyToManyField('Genres', blank=True)
    title = models.CharField(max_length=100, )
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2023)], blank=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = '"collection"."album"'
        verbose_name = _('album')
        verbose_name_plural = _('albums')
        

class Genres(UUIDMixin, CreatedMixin, ModifiedMixin):
    tracks = models.ManyToManyField(Tracks, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(_('description'), blank=True, null=True)
    
    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = '"collection"."genre"'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Client(CreatedMixin, ModifiedMixin):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    tracks = models.ManyToManyField(Tracks, blank=True)
    money = models.DecimalField(
    max_digits=config.DECIMAL_MAX_DIGITS,
    decimal_places=config.DECIMAL_PLACES,
    default=0,
)
    class Meta:
        db_table = '"collection"."client"'
        verbose_name = _('client')
        verbose_name_plural = _('client')

# Таблицы связи

class TrackGenre(UUIDMixin, CreatedMixin):
    track = models.ForeignKey(Tracks, on_delete=models.CASCADE, null=True )
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE, null=True )

    class Meta:
        db_table = '"collection"."track_genre"'
        unique_together = (('track', 'genre'),)

class AlbumGenre(UUIDMixin, CreatedMixin):
    album = models.ForeignKey(Albums, on_delete=models.CASCADE, null=True )
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE, null=True )

    class Meta:
        db_table = '"collection"."album_genre"'
        unique_together = (('album', 'genre'),)

class TrackAlbum(UUIDMixin, CreatedMixin):
    artist = models.ForeignKey(Artists, on_delete=models.CASCADE, null=True )
    album = models.ForeignKey(Albums, on_delete=models.CASCADE, null=True )
    track = models.ForeignKey(Tracks, on_delete=models.CASCADE, null=True )

    class Meta:
        db_table = '"collection"."track_album"'
        unique_together = (('track', 'album'),)

class ArtistAlbum(UUIDMixin, CreatedMixin):
    artist = models.ForeignKey(Artists, on_delete=models.CASCADE, null=True )
    album = models.ForeignKey(Albums, on_delete=models.CASCADE, null=True )

    class Meta:
        db_table = '"collection"."artist_album"'
        unique_together = (('artist', 'album'),)

class TrackClient(UUIDMixin, CreatedMixin):
    track = models.ForeignKey(Tracks, on_delete=models.CASCADE, null=True )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True )

    class Meta:
        db_table = '"collection"."track_client"'
        unique_together = (('track', 'client'),)
