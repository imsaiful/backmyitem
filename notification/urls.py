from django.conf.urls import url
from . import views


app_name = 'notifications'
urlpatterns = [
    url(r'^$', views.mynotification, name='mynotification'),
    url(r'^show/(?P<notification_id>[0-9]+)/$', views.show_notification, name='show_notification'),
    url(r'^read/(?P<notification_id>\d+)/$', views.read_notification, name='read_notification'),
    url(r'^request/(?P<pk>[0-9]+)/$', views.RequestItem.as_view(), name='request'),
]
