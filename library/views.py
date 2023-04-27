from django.shortcuts import render, get_object_or_404
from .models import Genre, Author, Book, BookInstance
from django.views import generic


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


def authors(request):
    authors = Author.objects.all()
    return render(request, 'authors.html', {'authors': authors})


def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author.html', {'author': single_author})


class BookListView(generic.ListView):
    model = Book
    template_name = "book_list.html"


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'

