from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^main$',views.index),
    url(r'^register$',views.register),
    url(r'^login$',views.login),
    url(r'^travels$',views.home),
    url(r'^logout$',views.logout),
    url(r'^travels/add$',views.add),
    url(r'^travels/add/trip$',views.addtrip),
    url(r'^travels/join$',views.join),
    url(r'^travels/destination/(?P<destination_id>\d+)$',views.destination)
]
