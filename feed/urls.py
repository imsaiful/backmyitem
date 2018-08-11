from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView

app_name = 'feed'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^report$', views.ReportCreate.as_view(), name='report'),
    url(r'^claimForm/(?P<pk>[0-9]+)/$', views.ClaimForm.as_view(), name='claim'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.ReportDetail.as_view(), name='detail'),
    url(r'^category/(?P<slug>\w+)/$', views.SearchCtaegoryView.as_view(), name='category'),
    url(r'^signup$', views.SignUpForm.as_view(), name='signup'),
    url(r'^login$', views.LoginForm.as_view(), name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^u/(?P<username>\w+)/$', views.Profile, name='profile'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.ReportUpdate.as_view(), name='report-update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.ReportDelete.as_view(), name='report-delete'),



]
