from django.shortcuts import render
from .models import Genre, Author, Book, BookInstance


def index(request):
    book_count = Book.objects.all().count()
    book_instance_count = BookInstance.objects.all().count()
    available_books_count = BookInstance.objects.filter(book_status__exact='a').count()

    author_count = Author.objects.all().count()

    context = {
        'books': book_count,
        'book_instances': book_instance_count,
        'authors': author_count,
        'available': available_books_count
    }

    return render(request, "index.html", context)
