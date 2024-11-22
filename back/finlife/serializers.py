from rest_framework import serializers
from .models import DepositOptions, DepositProducts, SavingProducts, SavingOptions


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
        fields = ['id', 'dcls_month', 'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 
                  'options', 'favorite_count', 'is_favorited', 'join_way', 'mtrt_int', 'spcl_cnd',
                  'join_deny', 'join_member', 'etc_note', 'max_limit', 'dcls_strt_day', 'dcls_end_day', 'fin_co_subm_day'
                  ]

    # 즐겨찾기 숫자 
    def get_favorite_count(self, obj):
        # related_name이 'favorited_deposit_products'로 변경되었으므로 수정
        return obj.favorited_by.count()
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            return user.is_authenticated and obj.favorited_by.filter(id=user.id).exists()
        return False

class SavingOptionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SavingOptions
        fields = ['intr_rate_type_nm', 'rsrv_type_nm', 'intr_rate', 'intr_rate2', 'save_trm']

class SavingProductsSerializer(serializers.ModelSerializer):
    options = SavingOptionsSerializer(many=True, read_only=True)
    favorite_count = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = SavingProducts
        fields = ['id', 'dcls_month', 'fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 
                  'options', 'favorite_count', 'is_favorited', 'join_way', 'mtrt_int', 'spcl_cnd',
                  'join_deny', 'join_member', 'etc_note', 'max_limit', 'dcls_strt_day', 'dcls_end_day', 'fin_co_subm_day'
                  ]
        
    # 즐겨찾기 숫자 
    def get_favorite_count(self, obj):
        # related_name이 'favorited_deposit_products'로 변경되었으므로 수정
        return obj.favorited_by.count()

    # 즐겨찾기 확인
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            return user.is_authenticated and obj.favorited_by.filter(id=user.id).exists()
        return False
