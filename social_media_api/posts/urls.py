from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, LikePostView, UnlikePostView
from django.urls import path

router = DefaultRouter()
router.register(r'', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls + [
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]

