"""Сериализаторы для моделей Post, Group и Comment. """
from rest_framework import serializers

from posts.models import Comment, Group, Post


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.
    Отображает данные поста, включая автора и группу.
    Автор доступен только для чтения.
    """
    author = serializers.StringRelatedField(read_only=True)
    group = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field='slug',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    Используется для отображения всех полей комментария.
    Автор и пост доступны только для чтения.
    """
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
