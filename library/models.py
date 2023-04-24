from django.db import models
import uuid


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField('Name', max_length=100, help_text="Enter type of genre: ")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    first_name = models.CharField("First name", max_length=100)
    last_name = models.CharField("Last name", max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"

    def display_books(self):
        return ', '.join(book.title for book in self.books.all())


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books')
    title = models.CharField('Title', max_length=200, help_text="Enter book title: ")
    description = models.TextField('Description', max_length=1000, help_text="Enter short book description: ")
    isbn = models.CharField(
        'ISBN', max_length=13,
        help_text='ISBN nr.: <a href="https://www.isbn-international.org/content/what-isbn">ISBN kodas</a>'
    )
    genre = models.ManyToManyField(Genre, help_text="Enter books genre: ")

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all())


class BookInstance(models.Model):
    instance_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique book UUID code")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    due_back = models.DateField("Available on:", null=True, blank=True)

    LOAN_STATUS = (
        ('p', 'Processing'),
        ('t', 'Taken'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    book_status = models.CharField(max_length=1, default='a', blank=True, choices=LOAN_STATUS, help_text='Book status')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f"{self.book.title}"


