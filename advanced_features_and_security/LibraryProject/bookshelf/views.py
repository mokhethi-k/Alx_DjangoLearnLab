from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from .forms import ExampleForm

# Create your views here.
@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    form = ExampleForm(request.GET or None)
    books = Book.objects.all()
    if form.is_valid():
        search = form.cleaned_data['search']
        books = books.filter(title__icontains=search)
    context = {'books': books}
    return render(request, 'bookshelf/book_list.html', context)


@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author_id = request.POST.get('author') 
        published_date = request.POST.get('published_date')
        author = get_object_or_404(Book.author, pk=author_id)

        Book.objects.create(title=title, author=author, published_date=published_date)
        return redirect('book_list')
    
    authors = Book.author.objects.all()
    return render(request, 'bookshelf/book_form.html', {'authors': authors})


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.title = request.POST.get('title')
        author_id = request.POST.get('author')
        book.author = get_object_or_404(Book.author, pk=author_id)
        book.published_date = request.POST.get('published_date')
        book.save()
        return redirect('book_list')

    authors = Book.author.objects.all()
    return render(request, 'bookshelf/book_form.html', {'book': book, 'authors': authors})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})








def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request,'bookshelf/register.html', context)