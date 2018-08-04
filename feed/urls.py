from django.conf.urls import url
from . import views


app_name='feed'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^report$', views.ReportCreate.as_view(), name='report'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.ReportDetail.as_view(), name='report'),
]