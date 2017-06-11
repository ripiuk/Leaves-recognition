from django.conf.urls import url
from . import views

app_name = 'recognition'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<id>\d+)/$', views.recognition, name='recognition'),
    url(r'^all_pictures/$', views.ShowAll.as_view(), name='all_pic'),
    url(r'^account/$', views.PersonalAcc.as_view(), name='personal_acc'),
    url(r'^search_result/?$', views.SearchList.as_view(), name='search'),
]
