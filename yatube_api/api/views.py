from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления постами.
    Доступ разрешен только авторизованным пользователям.
    Пользователь может изменять и удалять только свои посты.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Установка текущего пользователя автором поста при его создании.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Прооверка, что автор поста — текущий пользователь."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """
        Прооверка, что автор поста — текущий пользователь перед удалением.
        """
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Управления группами. Доступен только для чтения.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Управление комментариями."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        """
        Возвращение списка комментариев для конкретного поста.
        """
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """
        Создание комментария, связывая его с текущим пользователем и постом.
        """
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)

    def perform_update(self, serializer):
        """
        Проверка, что автор комментария — текущий пользователь.
        """
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого комментария запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """
        Автор комментария — текущий пользователь перед его удалением.
        """
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого комментария запрещено!')
        super().perform_destroy(instance)
