from rest_framework import serializers
from django.contrib.auth import get_user_model
from finlife.serializers import DepositProductsSerializer

User = get_user_model()

# 회원정보변경
class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'first_name', 'last_name']
        read_only_fields = ['username', 'name']

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

# 유저 프로필
class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    favorite_products_count = serializers.SerializerMethodField()
    favorite_products = DepositProductsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'followers_count', 'following_count', 'favorite_products_count', 'favorite_products']
        read_only_fields = ['username']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_favorite_products_count(self, obj):
        return obj.favorite_products.count()

# 비밀번호 변경
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

