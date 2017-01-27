from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register_process$', views.register_process),
    url(r'^login_process$', views.login_process),
    # url(r'^show_home/(?P<id>\d+)$', views.show_home),
    url(r'^show_home$', views.show_home),
    url(r'^add_quote$', views.add_quote),
    url(r'^add_to_my_favorites/(?P<id>\d+)$', views.add_show_my_favorites),
    url(r'^logout$', views.logout),
]
