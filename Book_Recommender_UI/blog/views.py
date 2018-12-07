from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Book


def home(request):
    context = {
        'books': Book.objects.all()
    }
    return render(request, 'blog/home.html', context)


class BookListView(ListView):
    model = Book
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'books'
    ordering = ['YearofPublication']
    paginate_by = 5


class UserBookListView(ListView):
    model = Book
    template_name = 'blog/user_books.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'books'
    paginate_by = 5


class BookDetailView(DetailView):
    model = Book


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['ISBN', 'Title', 'Author', 'YearofPublication', 'Publisher']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    fields = ['ISBN', 'Title', 'Author', 'YearofPublication', 'Publisher']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.Author:
            return True
        return False


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    success_url = '/'

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.Author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def books(request):
    return render(request, 'blog/books.html', {'title': 'Books'})

def reviews(request):
    return render(request, 'blog/user_reviews.html', {'title': 'About'})

def recommendations(request):
    return render(request, 'blog/user_recommendations.html', {'title': 'About'})