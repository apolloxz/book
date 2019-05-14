"""book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^register/$', views.register),
    url(r'^books/add/$', views.book_add),
    url(r'^publish/add/$', views.publish_add),
    url(r'^author/add/$', views.author_add),
    url(r'^book/(?P<pk>\d+)/change/$', views.book_edit),
    url(r'^book/(?P<pk>\d+)/delete/$', views.book_del),
    url(r'^publish_book/(?P<pk>\d+)/list/$', views.publish_book_list),
    url(r'^author_book/(?P<pk>\d+)/list/$', views.author_book_list),
]