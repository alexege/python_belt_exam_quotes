from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^add_quote$', views.add_quote),
    url(r'^add_to_favorites/(?P<id>\d+)$', views.add_to_favorites),
    url(r'^remove_from_favorites/(?P<id>\d+)$', views.remove_from_favorites),
    url(r'^users/(?P<id>\d+)$', views.show_user_info),
    url(r'^logout$', views.logout),
]