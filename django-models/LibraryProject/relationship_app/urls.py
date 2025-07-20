from django.urls import path
from .views import list_books, LibraryDetailView, RegisterView, UserLoginView, UserLogoutView
urlpatterns = [
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('', list_books, name='book_list' ),
]