from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register_process$', views.register_process),
    url(r'^login_process$', views.login_process),
    url(r'^show_home$', views.show_home),
    url(r'^add_appt$', views.add_appt),
    url(r'^edit_appt/(?P<appt_id>\d+)$', views.edit_appt),
    url(r'^delete_appt/(?P<appt_id>\d+)$', views.delete_appt),
    url(r'^update_appt/(?P<appt_id>\d+)$', views.update_appt),
    url(r'^logout$', views.logout),
]
