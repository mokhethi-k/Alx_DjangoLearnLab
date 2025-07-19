from django.urls import path
from .views import list_books, LibraryDetailView
urlpatterns = [
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('', list_books, name='book_list' ),
]