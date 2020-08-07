from django.urls import path

from . import views

app_name="encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entrypage, name="entrypage"),
    path("newpage", views.newpage, name="newpage"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("randompage", views.randompage, name="randompage")
]
