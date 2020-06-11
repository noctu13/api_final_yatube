from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Post, Comment, Follow, Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        fields = ("id", "author", "post", "text", "created")
        model = Comment
        extra_kwargs = {
            "post": {
                "required": False,
                #'write_only': True
            }
        }


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        fields = ("user", "following")
        model = Follow

    def validate(self, attrs):
        following = attrs["following"]
        user = self.context["request"].user
        if (
            user == following
            or Follow.objects.filter(user=user, following=following).exists()
        ):
            raise ValidationError()
        return attrs


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title")
        model = Group
