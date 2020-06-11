from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from .models import Post, Comment, Follow, Group
from .serializers import (
    PostSerializer,
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
)
from .permissions import IsOwnerOrReadOnly


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get("group", None)
        if group:
            queryset = queryset.filter(group=group)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get("post_id"))

    def get_queryset(self):
        return Comment.objects.filter(post=self.get_post())

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["=following__username", "=user__username"]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class GroupViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsOwnerOrReadOnly]
