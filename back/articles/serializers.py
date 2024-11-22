from rest_framework import serializers
from .models import Article, Comment
from accounts.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='like_users.count', read_only=True)  # 좋아요 수 추가

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'like_users')

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='like_users.count', read_only=True)  # 좋아요 수 추가

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'article', 'like_users')
