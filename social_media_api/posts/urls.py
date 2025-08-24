from django.urls import path, include
from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet, FeedView

# Base router
router = routers.SimpleRouter()
router.register(r"posts", PostViewSet, basename="post")

# Nested router for comments
posts_router = routers.NestedSimpleRouter(router, r"posts", lookup="post")
posts_router.register(r"comments", CommentViewSet, basename="post-comments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(posts_router.urls)),
    path("feed/", FeedView.as_view(), name="feed"),
]
