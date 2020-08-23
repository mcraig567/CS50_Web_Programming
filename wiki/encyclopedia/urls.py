from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("new", views.new, name="new"),
    path("<str:title>/edit", views.edit, name="edit"),
    path("randsite", views.randsite, name="randsite"),
    path("error/<int:message>", views.error, name="error")

]
