from rest_framework import serializers
from .models import DepositOptions, DepositProducts


class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        # 금리 유형, 금리, 최고 우대 금리, 저축 기간
        fields = ['intr_rate_type_nm', 'intr_rate', 'intr_rate2', 'save_trm']


class DepositProductsSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True)
    favorite_count = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = DepositProducts
        fields = ['id', 'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'options', 'favorite_count', 'is_favorited']

    # 즐겨찾기 숫자 
    def get_favorite_count(self, obj):
        return obj.favorited_by.count()

    # 즐겨찾기 확인
    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.favorited_by.filter(user=user).exists()


