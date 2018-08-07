from django.conf.urls import url
from . import views


app_name = 'feed'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^report$', views.ReportCreate.as_view(), name='report'),
    url(r'^claimForm/(?P<pk>[0-9]+)/$', views.ClaimForm.as_view(), name='claim'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.ReportDetail.as_view(), name='detail'),
    url(r'^category/(?P<slug>\w+)/$', views.SearchCtaegoryView.as_view(), name='category'),
    url(r'^signup$', views.SignUpForm.as_view(), name='signup')
]
