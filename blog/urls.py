from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<str:category>", views.category, name="category"),
    path("search", views.search, name="search"),
    path("post/<str:post_id>", views.post, name="post")
]