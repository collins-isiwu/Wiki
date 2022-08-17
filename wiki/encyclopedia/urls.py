from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"), 
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.random, name="random")
]
