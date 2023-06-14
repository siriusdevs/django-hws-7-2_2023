from django.shortcuts import render
from .models import Tracks, Albums, Artists, Genres, Client, TrackClient
from django.views.generic import ListView
from . import config
from django.db import transaction
from django.contrib.auth import mixins, decorators as auth_decorators
from .forms import AddFundsForm, RegistrationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from .serializers import TrackSerializer, ArtistSerializer, GenreSerializer, AlbumSerializer, ClientSerializer
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status as status_codes, parsers, decorators
import os 
from mutagen.mp3 import MP3
from pathlib import Path
from datetime import timezone, datetime
import requests
from django.core.exceptions import ValidationError


# Эта функция отвечает за регистрацию нового пользователя на сайте.

def register(request):
    form_errors = None
    if request.method == 'POST': 
        form = RegistrationForm(request.POST) # Сначала проверяется метод передачи данных, если метод POST, то данный запрос является запросом на создание нового пользователя - форма будет заполнена и отправлена на сервер.
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
            return HttpResponseRedirect(reverse('profile'))
        form_errors = form.errors
    return render(
        request,
        config.TEMPLATE_REGISTER,
        context={
            'form': RegistrationForm(),
            'form_errors': form_errors,
        },
    )


class TrackPage(viewsets.ModelViewSet):
    serializer_class = TrackSerializer

    def __init__(self, title, artist, duration, audio_file):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.audio = audio_file

    def display_info(self):
        print(f"{self.title} by {self.artist} ({self.duration})")
        audio = MP3(self.audio)

def track_page(request, track_id):
    # Получаем ссылку на аудиофайл (например, из базы данных или из API)
    folder_path = Path('/home/sirius/homework_django_project/django-hws-7-2_2023/collection/static/audio_files')
    music_files = list(folder_path.glob('*.mp3'))
    audio_url = music_files[int(track_id) - 1].name

    # Получаем информацию о треках
    playlist = Tracks.objects.all()
    track_pages = []

    # Создаем объекты TrackPage и добавляем их в список
    for track in playlist:
        track_page = TrackPage(track.title, track.artist, track.duration, folder_path / track.audio_url)
        track_pages.append(track_page)

    # Выводим информацию о всех треках ()
    for track_page in track_pages:
        track_page.display_info()
    
    return render(request, 'track_list.html', {'tracks': playlist})

from django.http import HttpResponse
from django.shortcuts import render

def track_list(request):
    if request.method == 'POST':
        # Обработка POST-запроса
        # Получение данных из формы
        track_name = request.POST.get("track_name", "Example")
        artist_name = request.POST.get("artist_name", "Artist")
        # Сохранение данных в базу данных или файл
        # Отображение страницы с результатами
        return HttpResponse(f"<h2>Title: {track_name}  Year: {artist_name}</h2>"), #render(request, 'tracks_list.html', {'track_name': track_name, 'artist_name': artist_name})
    else:
        # Отображение страницы с формой для ввода данных
        return render(request, 'tracks.html')



class Permission(permissions.BasePermission):
    safe_methods = ('GET', 'HEAD', 'OPTIONS', 'PATCH')
    unsafe_methods = ('POST', 'PUT', 'DELETE')

    def has_permission(self, request, _):
        if request.method in self.safe_methods:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in self.unsafe_methods:
            return bool(request.user and request.user.is_superuser)
        return False

@auth_decorators.login_required
def listen_music(request):
    context = {}
    client = Client.objects.get(user=request.user)
    track_id = request.GET.get('id')
    try:
        track = Tracks.objects.get(id=track_id)
    except Exception:
        track = None
    try:
        context['user_access'] = bool(client.tracks.get(id=track))
    except Exception:
        context['user_access'] = False

    if track:
        context['track'] = track
        context['audio_url'] = os.path.join(config.MEDIA_ROOT, track.audio_file.name)
        
        if request.method == 'POST':
            playlist = list(client.tracks.all().order_by('order'))
            current_index = playlist.index(track)
            if 'next' in request.POST and current_index < len(playlist) - 1:
                track = playlist[current_index + 1]
            elif 'previous' in request.POST and current_index > 0:
                track = playlist[current_index - 1]
            context['track'] = track
            context['audio_url'] = os.path.join(config.MEDIA_ROOT, track.audio_file.name)

    return render(request, config.TEMPLATE_LISTEN, context=context)


##############################################################
# Youtube AudioLibrary API

@decorators.api_view(['GET'])
def tracks_api(request):
    search_query = request.GET.get('query')
    if not search_query:
        return Response(
            'No search query provided',
            status=status_codes.HTTP_400_BAD_REQUEST,
        )
    try:
        tracks_info = get_tracks_info(search_query)
        if not tracks_info:
            return Response(
                f'No tracks found for search query: {search_query}',
                status=status_codes.HTTP_404_NOT_FOUND,
            )
        tracks_data = serialize_tracks_info(tracks_info)
        return Response(tracks_data, status=status_codes.HTTP_200_OK)
    except Exception:
        return Response(
            'Failed to retrieve tracks data',
            status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
def get_tracks_info(search_query):
    # Используем requests для выполнения запроса к YouTube Audio Library API
    response = requests.get(f'https://www.youtube.com/audiolibrary_ajax?action=qs_search&keyword={search_query}&type=audio&video_id=')
    # Если запрос успешен, получаем данные в формате JSON
    if response.ok:
        data = response.json()

        tracks_info = data.get('data').get('audioLibraries')
        return tracks_info
    raise Exception('Failed to retrieve tracks data')

def serialize_tracks_info(tracks_info):
    # Создаем пустой список для хранения сериализованных данных о треках
    tracks_data = []

    for track_info in tracks_info:
        track_data = {
            'id': track_info.get('id'),
            'title': track_info.get('title'),
            'artist': track_info.get('author'),
            'duration': track_info.get('duration'),
            'thumbnail_url': track_info.get('thumbnailUrl'),
            'download_url': track_info.get('downloadUrl'),
        }
        # Добавляем сериализованные данные о треке в список
        tracks_data.append(track_data)
    return tracks_data

################################################################


def custom_main(request):
    return render(
        request,
        config.TEMPLATE_MAIN,
        context={
            'tracks': Tracks.objects.all().count(),
            'genres': Genres.objects.all().count(),
            'artists': Artists.objects.all().count(),
            'albums': Albums.objects.all().count(),

        },
    )

def collection_view(cls_model, context_name, template): 
    class CustomListView(mixins.LoginRequiredMixin, ListView): 
        model = cls_model
        template_name = template
        paginate_by = config.PAGINATOR_THRESHOLD
        context_object_name = context_name   
     
    # GET на адресе, связанном  с этим представлением:
    # формирует контекст и список объектов (instances) с заданной модели (cls_model). 

        def get_context_data(self, **kwargs):             
            context = super().get_context_data(**kwargs)
            instances = cls_model.objects.all()
            paginator = Paginator(instances, config.PAGINATOR_THRESHOLD)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{context_name}_list'] = page_obj
            return context

    return CustomListView


def entity_view(cls_model, name, template):
    @auth_decorators.login_required
    def view(request):
        target_id = request.GET.get('id', '')
        context = {name: cls_model.objects.get(id=target_id)}
        return render(
            request,
            template,
            context=context,
        )
    return view
    
TracksListView = collection_view(Tracks, 'tracks', config.TRACKS_LIST)
AlbumsListView = collection_view(Albums, 'albums', config.ALBUMS_LIST)
ArtistsListView = collection_view(Artists, 'artists', config.ARTISTS_LIST)
GenresListView = collection_view(Genres, 'genres', config.GENRES_LIST)

track_view = entity_view(Tracks, 'track', config.TRACK_ENTITY)
genre_view = entity_view(Genres, 'genre', config.GENRE_ENTITY)
artist_view = entity_view(Artists, 'artist', config.ARTIST_ENTITY)
album_view = entity_view(Albums, 'album', config.ALBUM_ENTITY)



@transaction.atomic
@auth_decorators.login_required
def profile_page(request):
    user = request.user
    client = Client.objects.get(user=user)
    form_errors = []

    if request.method == 'POST':
        form = AddFundsForm(request.POST)

        if form.is_valid():
            funds_to_add = form.cleaned_data.get('money')
            if funds_to_add > 0:
                client.money += funds_to_add
                try:
                    client.save()
                except Exception as error:
                    form_errors.append(str(error))
                else:
                    return HttpResponseRedirect(reverse('profile'))
        else:
            form_errors.extend(form.errors.get('money'))
    user_data = {
        'username': user.username,
        'first name': user.first_name,
        'last name': user.last_name,
        'email': user.email,
        'money': client.money,
    }
    client_tracks = TrackClient.objects.filter(client=client)

    return render(
        request,
        config.TEMPLATE_PROFILE,
        context={
            'form': AddFundsForm(),
            'user_data': user_data,
            'form_errors': '; '.join(form_errors),
            'tracks': [track_client.track.title for track_client in client_tracks],
        },
    )

@auth_decorators.login_required
def subscription_purchase_page(request):
    client = Client.objects.get(user=request.user)
    price = config.SUBSCRIPTION_PRICE
    show_text = 'Subscribe'
    tracks = Tracks.objects.all()

    if request.method == 'POST' and client.money >= price:
        with transaction.atomic():
            client.money -= price
            client.subscription_expiry = timezone.now() + datetime.timedelta(days=config.SUBSCRIPTION_DAYS)
            client.save()

        return HttpResponseRedirect(reverse('track'))
    
    #TODO  добавить в Клиента поля 
    return render(
        request,
        template_name=config.TEMPLATE_PURCHASE_SUBSCRIPTION,
        context={
            'option': 'subscription',
            'track': None,
            'tracks': tracks,
            'funds': client.money,
            'price': price,
            'expiration_date': client.subscription_expiry,
            'show_text': show_text,
            'enough_money': client.money - price >= 0,
        },
    )
#TODO добавить в Клиента поля 



#GET/POST?
def query_from_request(cls_serializer, request) -> dict:
    query = {}
    for field in cls_serializer.Meta.fields:
        obj_value = request.GET.get(field, '')
        if obj_value:
            query[field] = obj_value
    return query


def create_viewset(cls_model, serializer, order_field):
    class CustomViewSet(viewsets.ModelViewSet):
        queryset = cls_model.objects.all()
        serializer_class = serializer
        permission_classes = [Permission]

        def get_queryset(self):
            query = query_from_request(serializer, self.request)
            queryset = cls_model.objects.filter(**query) if query else cls_model.objects.all()
            return queryset.order_by(order_field)
        
        def delete(self, request):
            def response_from_objects(num):
                if not num:
                    message = f'DELETE for model {cls_model.__name__}: query did not match any objects'
                    return Response(message, status=status_codes.HTTP_404_NOT_FOUND)
                status = status_codes.HTTP_204_NO_CONTENT if num == 1 else status_codes.HTTP_200_OK
                return Response(f'DELETED {num} instances of {cls_model.__name__}', status=status)

            query = query_from_request(serializer, request)
            if query:
                instances = cls_model.objects.all().filter(**query)
                num_objects = len(instances)
                try:
                    instances.delete()
                except Exception as error:
                    return Response(error, status=status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
                return response_from_objects(num_objects)
            return Response('DELETE has got no query', status=status_codes.HTTP_400_BAD_REQUEST)

        def put(self, request):
            # gets id from query and updates instance with this ID, creates new if doesnt find any.
            def serialize(target):
                attrs = parsers.JSONParser().parse(request)
                model_name = cls_model.__name__
                if target:
                    serialized = serializer(target, data=attrs, partial=True)
                    status = status_codes.HTTP_200_OK
                    body = f'PUT has updated {model_name} instance'
                else:
                    serialized = serializer(data=attrs, partial=True)
                    status = status_codes.HTTP_201_CREATED
                    body = f'PUT has created new {model_name} instance'
                if not serialized.is_valid():
                    return (
                        f'PUT could not serialize query {query} into {model_name}',
                        status_codes.HTTP_400_BAD_REQUEST,
                    )
                try:
                    model_obj = serialized.save()
                except Exception as error:
                    return error, status_codes.HTTP_500_INTERNAL_SERVER_ERROR
                body = f'{body} with id={model_obj.id}'
                return body, status

            query = query_from_request(serializer, request)
            target_id = query.get('id', '')
            if not target_id:
                return Response('PUT has got no id', status=status_codes.HTTP_400_BAD_REQUEST)
            try:
                target_object = cls_model.objects.get(id=target_id)
            except Exception:
                target_object = None
            message, status = serialize(target_object)
            return Response(message, status=status)


    return CustomViewSet

TracksViewSet = create_viewset(Tracks, TrackSerializer, 'title')
ArtistsViewSet = create_viewset(Artists, ArtistSerializer, 'name')
GenresViewSet = create_viewset(Genres, GenreSerializer, 'title')
AlbumsViewSet = create_viewset(Albums, AlbumSerializer, 'title')





# 1 Проверить, что функция соответсвует отображение во views
# 2 Проверить запросы/ они есть в библиотеке + Postman
# 3 Написать тесты на рест
# 4 Странички

# Должно в urls быть отображено  
# profile_page
# listen_music
# track_page
# subscription_purchase_page

# 1366x768
# css для плашек
