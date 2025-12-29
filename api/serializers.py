from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Post, Comment

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'text',
            'pub_date',
            'image',
            'category',
            'location',
            'is_published',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'text',
            'created_at',
            'post',
        )
