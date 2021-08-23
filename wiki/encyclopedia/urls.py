from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
	path("create", views.CreatePage, name="pageCreate"),
    path("random", views.RandomPage, name="random"),
    path("edit", views.EditPage, name="editInput"),
    path("edit/<str:name>", views.EditPage, name="edit"),
	path("<str:name>", views.FindPage, name="pageSearchURL")
]
