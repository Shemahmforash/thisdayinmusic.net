"""thisdayinmusic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from events import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^events/(?P<month>\w+)/(?P<day>\d{1,2})$',
        views.events_page, name="events"),
    url(r'^playlist$', views.playlist_page, name='playlist'),
    url(r'^playlist/(?P<month>\w+)/(?P<day>\d{1,2})$$', views.playlist_page, name='playlist_with_date'),
    url(r'^playlist/create_playlist$', views.add_to_spotify, name='add_to_spotify'),
    url(r'^playlist/create_playlist/callback$', views.add_to_spotify_callback, name='add_to_spotify_callback'),
    url(r'^about$', views.about_page, name='about'),
]
