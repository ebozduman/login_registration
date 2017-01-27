from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register_process$', views.register_process),
    url(r'^login_process$', views.login_process),
    url(r'^show_home/(?P<id>\d+)$', views.show_home),
    url(r'^logout', views.logout),
]
