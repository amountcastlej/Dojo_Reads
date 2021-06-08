from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index), 
    path('register', views.register), 
    path('login', views.login), 
    path('books', views.books), 
    path('books/add', views.add), 
    path('books/create', views.create), 
    path('books/<int:book_id>', views.book), 
    path('books/<int:book_id>/review', views.add_review), 
    path('books/<int:book_id>/delete_review/<int:review_id>', views.delete),
    path('users/<int:user_id>', views.user), 
    path('logout', views.logout),
] 








