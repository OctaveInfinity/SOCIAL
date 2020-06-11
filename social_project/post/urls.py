from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)


urlpatterns = [
    path('', PostListView.as_view(), name='dj-post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='dj-post-detail'),
    path('create/', PostCreateView.as_view(), name='dj-post-create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='dj-post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='dj-post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='dj-user-posts'),
]