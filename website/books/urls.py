from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_home),
    path('home', views.book_home),
    path('list', views.book_list),
    path('add', views.book_add),
    path('edit/<int:id>',views.book_edit),
    path('delete/<int:id>',views.book_delete),
    path('search', views.book_search),
    path('dosearch', views.book_dosearch)
]