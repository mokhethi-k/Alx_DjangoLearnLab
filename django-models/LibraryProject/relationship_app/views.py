from django.shortcuts import render
from relationship_app.models import *
from django.views.generic import DetailView

# Create your views here.
def listBooks(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetail(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

