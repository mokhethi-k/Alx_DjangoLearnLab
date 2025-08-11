from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, UserLoginView, profile, home, PostDetail, PostList, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html', next_page='login'), name='logout'),
    path('profile/', profile, name='profile'),
    path('', home, name='home'),
    path('posts/', PostList.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/new/', PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
