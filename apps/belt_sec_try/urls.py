from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^delete/(?P<number>\d+)$', views.delete),
    url(r'^appointments/(?P<number>\d+)$', views.showedit),
    url(r'^makeedit/(?P<number>\d+)$', views.makeedit)
]