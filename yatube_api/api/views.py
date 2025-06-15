"""ViewSet-классы для работы с моделями Post, Group и Comment."""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from posts.models import Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для чтения данных о группах.
    Доступен только просмотр.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для полной CRUD-работы с постами.
    Только автор может редактировать или удалять свой пост.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Создаёт пост с автором текущим пользователем."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Запрещает редактирование чужого поста."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого поста запрещено!')
        serializer.save()

    def perform_destroy(self, instance):
        """Запрещает удаление чужого поста."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого поста запрещено!')
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с комментариями к постам.
    Комментарии вложены в посты и доступны только при указании post_id.
    Только автор может редактировать или удалять свои комментарии.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_post(self):
        """Возвращает пост."""
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Возвращает список комментариев к указанному посту."""
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Создаёт комментарий с текущим пользователем как автором."""
        serializer.save(author=self.request.user, post=self.get_post())

    def perform_update(self, serializer):
        """Запрещает редактирование чужого комментария."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого комментария запрещено!')
        serializer.save()

    def perform_destroy(self, instance):
        """Запрещает удаление чужого комментария."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого комментария запрещено!')
        instance.delete()
