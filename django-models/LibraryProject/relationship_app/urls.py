from django.urls import path
from .views import list_books, LibraryDetailView, Admin, Librarian, Member
from . import views
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register , name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('', list_books, name='book_list' ),
    path('admin-dashboard/', Admin, name='admin_view'),
    path('librarian-dashboard/', Librarian, name='librarian_view'),
    path('member-dashboard/', Member, name='member_view'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]