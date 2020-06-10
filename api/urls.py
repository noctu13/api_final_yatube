from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet


router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register(r'posts/(?P<post_id>[0-9]+)/comments', CommentViewSet, basename='comment')
router.register('group', GroupViewSet, basename='group')
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
]
