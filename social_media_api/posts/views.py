from rest_framework import viewsets,filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment,Post
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from .models import Post, Like
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def feed_view(request):

    following_users = request.user.following.all()

    Post.objects.filter(author__in=following_users).order_by("-created_at")

    serializer = PostSerializer(Post, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    # get the post
    post = get_object_or_404(Post, pk=pk)

    # create like if it doesn't exist
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response({"message": "Already liked"}, status=400)

    # create a notification for the post author if they are not the liker
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )

    return Response({"message": "Post liked"})


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    # get the post
    post = get_object_or_404(Post, pk=pk)

    # find existing like
    like = Like.objects.filter(user=request.user, post=post)

    if like.exists():
        like.delete()
        return Response({"message": "Post unliked"})

    return Response({"message": "You haven't liked this post"}, status=400)
