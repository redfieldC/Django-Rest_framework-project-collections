from django.urls import path
from .views import PostListView, PostCreateView,CommentCreateView

urlpatterns = [
    path('all-posts/', PostListView.as_view(), name='post-list'),  # Endpoint for listing posts with nested comments
    path('post-create/', PostCreateView.as_view(), name='post-create'),  # Endpoint for creating posts with nested comments
    path('comments-under-post/<int:post_id>/', CommentCreateView.as_view(), name='comment-create'),
]
