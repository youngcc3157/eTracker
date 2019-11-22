from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('api/', include('src.users.api.urls')),
]
