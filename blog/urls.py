from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^list/$', views.ListView.as_view(), name='list'),
    url(r'^drafts/$', views.DraftView.as_view(), name='drafts'),
    url(r'^article/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^article/new/$', views.post_new, name='new_post'),
    url(r'^article/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^article/(?P<pk>[0-9]+)/publish/$', views.post_pub, name='post_pub'),
    url(r'^article/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
]