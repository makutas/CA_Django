from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Author, Book, BookInstance
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import BookReviewForm, ProfileUpdateForm, UserUpdateForm
from django.views.generic.edit import FormMixin


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    template_name = "book_list.html"


class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
    form_class = BookReviewForm

    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.book_id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(BookDetailView, self).form_valid(form)


def index(request):
    book_count = Book.objects.all().count()
    book_instance_count = BookInstance.objects.all().count()
    available_books_count = BookInstance.objects.filter(book_status__exact='a').count()

    author_count = Author.objects.all().count()
    number_of_visits = request.session.get('number_of_visits', 1)
    request.session['number_of_visits'] = number_of_visits + 1

    context = {
        'books': book_count,
        'book_instances': book_instance_count,
        'authors': author_count,
        'available': available_books_count,
        'number_of_visits': number_of_visits
    }

    return render(request, "index.html", context)


def authors(request):
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    return render(request, 'authors.html', context={'authors': paged_authors})


def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author.html', {'author': single_author})


def search(request):
    # Ima informaciją iš paieškos laukelio
    query = request.GET.get('query')
    # Prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    # Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės didžiosios/mažosios.
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'search.html', {'books': search_results, 'query': query})


@csrf_protect
def register(request):
    if request.method == "POST":
        # Retrieve values from the form via POST request
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if the original and repeated passwords match
        if password != password2:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')

        # Check if username is taken
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Vartotojo vardas {username} užimtas!')
            return redirect('register')

        # Check if email is taken
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
            return redirect('register')

        # If the checks are passed, we can create a new User
        User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                 email=email, password=password)

        messages.info(request, f'Vartotojas {username} užregistruotas!')
        return redirect('login')

    return render(request, 'registration/register.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, f"Profilis atnaujintas")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)


# ----------------------------------------------------CRUD--------------------------------------------------------------
# -------------------------------------------------LIST VIEW------------------------------------------------------------

class UserBooksListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'user_books.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user).filter(book_status__exact='t').order_by('due_back')


@login_required(login_url='login')
def user_books(request):
    user = request.user
    try:
        user_books = BookInstance.objects.filter(reader=request.user).filter(book_status__exact='t').order_by(
            'due_back'
        )
    except BookInstance.DoesNotExist:
        user_books = None

    context = {
        'user': user,
        'user_books': user_books,
    }

    return render(request, 'user_books2.html', context)


# -------------------------------------------------DETAIL VIEW----------------------------------------------------------

class UserBookDetailView(LoginRequiredMixin, generic.DetailView):
    model = BookInstance
    template_name = 'user_book.html'


@login_required(login_url='login')
def user_book(request, pk):
    try:
        user_taken_book = BookInstance.objects.get(instance_id=pk)
    except BookInstance.DoesNotExist:
        user_taken_book = None

    context = {
        'user_taken_book': user_taken_book
    }

    return render(request, 'user_book2.html', context)


# -------------------------------------------------CREATE VIEW----------------------------------------------------------
class UserBookCreateView(LoginRequiredMixin, generic.CreateView):
    model = BookInstance
    template_name = 'create_new_book_instance.html'
    fields = ['book', 'due_back']
    success_url = '/library/my_books/'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        form.instance.book_status = 't'
        return super().form_valid(form)


def create_new_book_instance(request):
    """
    1. Reikalinga forma su fieldais kuriuos norim editint
    2. Pries darant save form mum reikia ideti useri (required nes yra FK)
    3. Urls/template/ analogiskai kaip sitie tik +2 (create2)
    4. Pasiziurekit get_or_create metoda prie to pacio (kai darai per query) sito nereiks cia
    :param request:
    :return:
    """
    # if request.method == 'POST':
    #     form = SomeForm(data=request.POST)
    #     if form.is_valid:
    #         add_user = form.save(False)
    #         add_user.reader = request.user
    #         add_user.save()
    # else:
    #     form = SomeForm()
    #
    # context = {
    #     'form': form
    # }
    # return render(request, 'some.html', context)
    pass


# -------------------------------------------------UPDATE VIEW----------------------------------------------------------
class UserBookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BookInstance
    template_name = 'update_book_instance.html'
    fields = ['book', 'due_back', 'book_status']
    success_url = '/library/my_books/'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        book_instance = self.get_object()
        return self.request.user == book_instance.reader


def update_book_instance(request, pk):
    pass


# -------------------------------------------------DELETE VIEW----------------------------------------------------------
class UserBookDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = BookInstance
    success_url = '/library/my_books/'
    template_name = 'delete_book_instance.html'

    def test_func(self):
        book_instance = self.get_object()
        return self.request.user == book_instance.reader


def delete_book_instance(request, pk):
    pass