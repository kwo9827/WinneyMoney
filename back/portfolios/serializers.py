from rest_framework import serializers
from .models import (
    Portfolio,
    Stock,
    Crypto,
    UserResponse,
    RecommendationLog,
    PortfolioDeposit,
    PortfolioSaving,
)
from finlife.models import DepositProducts, SavingProducts

# 추천 로그 Serializer
class RecommendationLogSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_type = serializers.SerializerMethodField()

    class Meta:
        model = RecommendationLog
        fields = [
            'product_name',
            'product_type',
            'reason',
            'recommended_allocation',
            'recommended_amount',
            'recommended_volatility',  # 추천 후 변동성 추가
            'created_at',
        ]

    def get_product_type(self, obj):
        """
        추천 상품 타입(Deposit or Saving) 반환.
        """
        if isinstance(obj.product, DepositProducts):
            return "Deposit"
        elif isinstance(obj.product, SavingProducts):
            return "Saving"
        return "Unknown"

    def get_product_name(self, obj):
        """
        추천 상품 이름 반환.
        """
        return obj.product.fin_prdt_nm if obj.product else "Unknown"


# 예금 Serializer
class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = ['id', 'kor_co_nm', 'fin_prdt_nm']


# 적금 Serializer
class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = ['id', 'kor_co_nm', 'fin_prdt_nm']


# PortfolioDeposit Serializer
class PortfolioDepositSerializer(serializers.ModelSerializer):
    deposit_product = DepositSerializer()  # 예금 상품 정보 포함

    class Meta:
        model = PortfolioDeposit
        fields = ['id', 'deposit_product', 'balance', 'created_at']


# PortfolioSaving Serializer
class PortfolioSavingSerializer(serializers.ModelSerializer):
    saving_product = SavingSerializer()  # 적금 상품 정보 포함

    class Meta:
        model = PortfolioSaving
        fields = ['id', 'saving_product', 'balance', 'created_at']


# 주식 Serializer
class StockSerializer(serializers.ModelSerializer):
    quantity = serializers.DecimalField(max_digits=15, decimal_places=6, read_only=True)
    current_investment = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    volatility = serializers.FloatField(read_only=True)

    class Meta:
        model = Stock
        fields = [
            'id',
            'ticker',
            'purchase_price',
            'total_investment',
            'quantity',
            'current_value',
            'current_investment',
            'volatility',
            'created_at',
        ]


# 암호화폐 Serializer
class CryptoSerializer(serializers.ModelSerializer):
    quantity = serializers.DecimalField(max_digits=15, decimal_places=6, read_only=True)
    current_investment = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    volatility = serializers.FloatField(read_only=True)

    class Meta:
        model = Crypto
        fields = [
            'id',
            'name',
            'symbol',
            'purchase_price',
            'total_investment',
            'quantity',
            'current_value',
            'current_investment',
            'volatility',
            'created_at',
        ]


# 포트폴리오 Serializer
class PortfolioSerializer(serializers.ModelSerializer):
    recommendation_logs = RecommendationLogSerializer(many=True, read_only=True)
    stocks = StockSerializer(many=True, read_only=True)
    cryptocurrencies = CryptoSerializer(many=True, read_only=True)
    deposits = PortfolioDepositSerializer(source="portfolio_deposits", many=True, read_only=True)
    savings = PortfolioSavingSerializer(source="portfolio_savings", many=True, read_only=True)
    total_investment = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    total_volatility = serializers.FloatField(read_only=True)
    allocation = serializers.JSONField(read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            'id',
            'user',
            'name',
            'total_investment',
            'total_volatility',
            'allocation',
            'predicted_economy',
            'risk_preference',
            'current_cash',
            'monthly_income',
            'stocks',
            'cryptocurrencies',
            'deposits',
            'savings',
            'recommendation_logs',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'user', 'created_at', 'updated_at', 'total_investment', 'total_volatility', 'allocation'
        ]


# 사용자 응답 Serializer
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['id', 'portfolio', 'current_step', 'responses']
