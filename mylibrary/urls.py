from collections import namedtuple
from django.urls import path

from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("authors", views.authors_view, name="authors"),
    path("search", views.search_view, name="search"),
    path("addauthors", views.add_author, name="addauthor"),
    path("books/new", views.addbooks_view, name="addbooks"),
    path("books/search", views.books_search_view, name="searchbooks"),
    path("authors/<str:author_id>", views.author_view, name = "authorview"),
    path("author/edit/<str:author_id>", views.author_edit, name = "authoredit"),
    path("book/edit/<str:book_id>", views.edit, name="edit"),
    path("book/delete/<str:book_id>", views.delete, name = "delete"),
    path("author/delete/<str:author_id>", views.delete_author, name = "deleteauthor"),
    path("book/detail/<str:book_id>", views.book_detail, name="bookdetail"),
]