from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, PostByTagListView, post_search, UserLoginView, profile, home, PostDetail, PostList, PostCreate, PostUpdate, PostDelete, CommentCreateView, CommentDeleteView, CommentUpdateView

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
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag'),
    path('search/', post_search, name='post_search'),
]
