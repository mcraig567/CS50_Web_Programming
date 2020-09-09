from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:list_id>", views.listing, name="listing"),
    path("listing/<int:list_id>/close", views.close, name="close"),
    path("listing/<str:user_name>/watch", views.watch, name="watch"),
    path("listing/<str:user_name>/<int:list_id>", views.watch_add, name="watch_add")

]
