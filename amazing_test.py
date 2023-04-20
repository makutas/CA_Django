import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from library.models import Book, Author


book = Book.objects.filter(book_id=1)

