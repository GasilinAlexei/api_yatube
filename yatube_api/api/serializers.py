from rest_framework import serializers
from posts.models import Post, Group, Comment


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'text', 'author', 'image', 'group', 'pub_date']


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Group.
    Используется для отображения информации о группах.
    """
    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    Поле post связано с моделью Post и является только для чтения.
    """
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text', 'created']
