from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets, authentication
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.reverse import reverse as drf_reverse
from rest_framework.response import Response

from post.models import Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, UserSerializer



@api_view(['GET'])
def api_root(request, format=None):
    """
    Root page for API-interface.
    """
    return Response({
        'users': drf_reverse('user-list', request=request, format=format),
        'posts': drf_reverse('post-list', request=request, format=format)
    })



class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset            = User.objects.all()
    serializer_class    = UserSerializer
    permission_classes  = [permissions.IsAdminUser]



class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset            = Post.objects.all()
    serializer_class    = PostSerializer
    permission_classes  = [permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class PostLikeAPIToggle(APIView):
    """
    This CBV provides customs functionality for 
    Like/Unlike actions via API-interface.
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, **kwargs):
        obj = get_object_or_404(Post, id=self.kwargs['pk'])
        user = self.request.user
        liked_flag = False
        
        if user.is_authenticated:
            if user in obj.liked.all():
                liked_flag = False
                obj.liked.remove(user)
            else:
                liked_flag = True
                obj.liked.add(user)
        
        data = {
            "liked_flag": liked_flag
        }
        return Response(data)
