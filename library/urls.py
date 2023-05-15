from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>', views.author, name='author'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('search/', views.search, name='search'),
    path('account/', include('django.contrib.auth.urls')),
    path('my_books/', views.UserBooksListView.as_view(), name='my-books'),
    path('my_books2/', views.user_books, name='my-books2'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
