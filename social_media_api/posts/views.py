from django.shortcuts import render

from rest_framework import viewsets, filters, status, generics
from rest_framework import permissions
from rest_framework.response import Response 
from rest_framework.views import APIView 
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend 
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly 
from notifications.models import Notification

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all() 
    serializer_class = PostSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = ['title', 'content'] 


    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # ALX check: use get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)

        # Get or create like
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # Notification
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )
            return Response({'status': 'Post liked'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'You already liked this post'}, status=status.HTTP_200_OK)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # ALX check: use get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)

        # Delete like if exists
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({'status': 'Post unliked'}, status=status.HTTP_200_OK)
        return Response({'status': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)            

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')  # drf-nested-routers passes post_pk
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        serializer.save(author=self.request.user, post_id=post_id) 

class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request):
        user = request.user 
        following_users = user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at') 
        serializer = PostSerializer(posts, many=True) 
        return Response(serializer.data) 