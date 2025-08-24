from rest_framework import viewsets, permissions, filters
from rest_framework import generics
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


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
