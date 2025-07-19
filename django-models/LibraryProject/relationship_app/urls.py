from django.urls import path
from .views import listBooks, LibraryDetail
urlpatterns = [
    path('library/<int:pk>/', LibraryDetail.as_view(), name='library_detail'),
    path('', listBooks, name='book_list' ),
]