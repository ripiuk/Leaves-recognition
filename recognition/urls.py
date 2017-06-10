from django.conf.urls import url
from . import views

app_name = 'recognition'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<id>\d+)/$', views.recognition, name='recognition'),
]
