from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import api_root, UserViewSet, PostViewSet


user_list   = UserViewSet.as_view({ 'get': 'list',
                                    'post': 'create' })

user_detail = UserViewSet.as_view({ 'get': 'retrieve',
                                    'put': 'update',
                                    'patch': 'partial_update',
                                    'delete': 'destroy' })


post_list   = PostViewSet.as_view({ 'get': 'list',
                                    'post': 'create' })  

post_detail = PostViewSet.as_view({ 'get': 'retrieve',
                                    'put': 'update',
                                    'patch': 'partial_update',
                                    'delete': 'destroy' })


# API endpoints
urlpatterns = format_suffix_patterns([
    path('',                        api_root,       name='api-root'),
    
    path('users/',                  user_list,      name='user-list'),
    path('users/<int:pk>/',         user_detail,    name='user-detail'),
    
    path('posts/',                  post_list,      name='post-list'),
    path('posts/<int:pk>/',         post_detail,    name='post-detail'),
])