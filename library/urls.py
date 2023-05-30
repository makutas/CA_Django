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
    # Class based views for BookInstance
    path('my_books/', views.UserBooksListView.as_view(), name='my-books'),
    path('my_books/<uuid:pk>', views.UserBookDetailView.as_view(), name='my-book'),
    path('my_books/create/', views.UserBookCreateView.as_view(), name='create'),
    path('my_books/create2/', views.create_new_book_instance, name='create2'),
    path('my_books/update/<uuid:pk>', views.UserBookUpdateView.as_view(), name='update'),
    path('my_books/update2/<uuid:pk>', views.update_book_instance, name='update2'),
    path('my_books/delete/<uuid:pk>', views.UserBookDeleteView.as_view(), name='delete'),
    path('my_books/delete2/<uuid:pk>', views.delete_book_instance, name='delete2'),
    # Function based views for BookInstance
    path('my_books2/', views.user_books, name='my-books2'),
    path('my_books2/<uuid:pk>', views.user_book, name='my-book2'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # TRANSLATE
    path('i18n/', include('django.conf.urls.i18n')),
]
