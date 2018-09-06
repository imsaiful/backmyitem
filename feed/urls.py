from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView


app_name = 'feed'
urlpatterns = [
    url(r'^$', views.IndexView, name='index'),
    url(r'^report$', views.ReportCreate.as_view(), name='report'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.ReportDetail.as_view(), name='detail'),
    url(r'^category/(?P<slug>\w+)/$', views.SearchItemType.as_view(), name='category'),
    url(r'^signup$', views.SignUpForm.as_view(), name='signup'),
    url(r'^login$', views.LoginForm.as_view(), name='login'),

    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^u/(?P<username>\w+)/$', views.Profile, name='profile'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.ReportUpdate.as_view(), name='report-update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.ReportDelete.as_view(), name='report-delete'),


    # notification

    url(r'^notification/$', views.mynotification, name='mynotification'),
    url(r'^read_notification/$', views.read_Notification, name='readnotification'),
    url(r'^notification/show/(?P<notification_id>\d+)/$', views.show_notification, name='show_notification'),
    url(r'^notification/read/(?P<notification_id>\d+)/$', views.read_notification, name='read_notification'),
    url(r'^notification/request/(?P<pk>[0-9]+)/$', views.RequestItem.as_view(), name='request'),


    #static pages
    url(r'^about/$', views.home_page, name='about'),
    url(r'^contact/$', views.Contact_page.as_view(), name='contact'),
    url(r'^team/$', views.TeamPage , name='team'),
    url(r'^privacy/$', views.privacy_page, name='privacy'),


]