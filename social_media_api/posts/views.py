from rest_framework import viewsets, permissions, filters, status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Only allow authors to edit or delete their own content."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        """Filter comments by the parent post id from the URL"""
        return Comment.objects.filter(post_id=self.kwargs["post_pk"]).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs["post_pk"])


class FeedView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get all the users the current user is following
        following_users = request.user.following.all()

        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    




class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        # 1. Use generics.get_object_or_404 instead of normal get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)

        # 2. Use get_or_create for Like
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            # 3. Create a notification for the post author
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )
            return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        post = generics.get_object_or_404(Post, pk=pk)

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)