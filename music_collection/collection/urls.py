"""music collection URL Configuration."""
from django.contrib import admin #Первой строкой из модуля django.contrib импортируется класс AdminSite, который предоставляет возможности работы с интерфейсом администратора.
from django.urls import path, include #торой строкой из модуля django.urls импортируется функция path. Эта функция задает сопоставление определенного маршрута с функцией обработки. 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('collection_app.urls')),
]