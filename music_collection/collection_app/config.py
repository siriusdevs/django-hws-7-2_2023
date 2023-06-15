import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'collection_app/static/audio_files')

CF_DEFAULT = 50
DECIMAL_MAX_DIGITS = 10
DECIMAL_PLACES = 2
EMAIL_LENGTH = 128

PAGINATOR_THRESHOLD = 20
# TEMPLATE_WEATHER = 'pages/weather.html'
TEMPLATE_PROFILE = 'pages/profile.html'
TEMPLATE_PURCHASE_SUBSCRIPTION = 'pages/purchase.html'
TEMPLATE_LISTEN = 'pages/listen.html'
TEMPLATE_REGISTER = 'registration/register.html' #рег
TEMPLATE_MAIN = 'index.html'
TEMPLATE_PLAYER = 'pages/player.html'


ENTITIES = 'entities'
TRACK_ENTITY = f'{ENTITIES}/track.html'
ARTIST_ENTITY = f'{ENTITIES}/artist.html'
GENRE_ENTITY = f'{ENTITIES}/genre.html'
ALBUM_ENTITY = f'{ENTITIES}/album.html'
# CHANEL_ENTITY = f'{ENTITIES}/chanel.html'

COLLECTION= 'collection'
TRACKS_LIST = f'{COLLECTION}/tracks.html'
ALBUMS_LIST = f'{COLLECTION}/albums.html'
ARTISTS_LIST = f'{COLLECTION}/artists.html'
GENRES_LIST = f'{COLLECTION}/genres.html'

SUBSCRIPTION_PRICE = 299
TRACK_PRICE = 59