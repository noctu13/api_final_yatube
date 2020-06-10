from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status

from .models import User, Post, Comment, Follow, Group
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer
from .permissions import IsOwnerOrReadOnly

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        queryset = Comment.objects.filter(post=post)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

class FollowViewSet(ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['=following__username', '=user__username']

    def perform_create(self, serializer):
        following = User.objects.get(username=self.request.data.get('following'))
        # if following == self.request.user:
        #     return ValidationError("User can't follow himself")
        return serializer.save(user=self.request.user, following=following)

class GroupViewSet(ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsOwnerOrReadOnly]
