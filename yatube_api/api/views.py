from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, mixins, filters

from .permissions import IsAuthorOrReadOnly
from posts.models import Post, Group, User
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_post(self):
        """Получить пост из переданного post_id"""
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Кверисет комментариев полученного поста"""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """
        Передать объект пользователя в поле user, полученный пост в поле post
        """
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    pass


class FollowViewSet(CreateRetrieveViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_user(self):
        """Получить аутентифицированного пользователя"""
        return get_object_or_404(User, username=self.request.user)

    def get_queryset(self):
        """Кверисет подписчиков аутентифицированного пользователя"""
        return self.get_user().follower.all()

    def perform_create(self, serializer):
        """Передать объект пользователя в поле user"""
        serializer.save(user=self.request.user)
