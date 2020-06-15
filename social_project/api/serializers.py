from rest_framework import serializers
from django.contrib.auth.models import User

from post.models import Post



class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner       = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model   = Post
        fields  =   [
            'url',
            'id',
            'title',
            'content',
            'liked_count',
            'owner'
        ]



class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts   = serializers.HyperlinkedRelatedField(
                                            many=True,
                                            view_name='post-detail',
                                            read_only=True
                                            )
    class Meta:
        model   = User
        fields  = [
            'url',
            'id',
            'username',
            'email',
            'posts'
        ]