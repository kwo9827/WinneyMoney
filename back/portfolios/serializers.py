from rest_framework import serializers
from .models import Portfolio, Stock, Crypto, UserResponse, RecommendationLog, PortfolioDeposit, PortfolioSaving
from finlife.models import DepositProducts, SavingProducts

# 추천 로그 Serializer
class RecommendationLogSerializer(serializers.ModelSerializer):
    product_id = serializers.SerializerMethodField()  # 상품 ID 필드 추가
    product_name = serializers.SerializerMethodField()
    product_type = serializers.SerializerMethodField()

    class Meta:
        model = RecommendationLog
        fields = ['product_id', 'product_name', 'product_type', 'reason', 'created_at']

    def get_product_id(self, obj):
        # object_id는 상품의 기본 키(PK)를 나타냅니다.
        return obj.object_id

    def get_product_type(self, obj):
        if isinstance(obj.product, DepositProducts):
            return "Deposit"
        elif isinstance(obj.product, SavingProducts):
            return "Saving"
        return "Unknown"

    def get_product_name(self, obj):
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
    quantity = serializers.DecimalField(
        max_digits=15, decimal_places=6, read_only=True  # 자동 계산 필드
    )
    volatility = serializers.FloatField(read_only=True)  # 변동성은 읽기 전용

    class Meta:
        model = Stock
        fields = [
            'id',
            'ticker',
            'purchase_price',
            'total_investment',
            'quantity',
            'current_value',
            'volatility',
            'created_at',
        ]

    def create(self, validated_data):
        validated_data['volatility'] = self.context.get('volatility')
        return super().create(validated_data)

# 암호화폐 Serializer
class CryptoSerializer(serializers.ModelSerializer):
    quantity = serializers.DecimalField(
        max_digits=15, decimal_places=6, read_only=True  # 자동 계산 필드
    )
    volatility = serializers.FloatField(read_only=True)  # 변동성은 읽기 전용

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
            'volatility',
            'created_at',
        ]

    def create(self, validated_data):
        validated_data['volatility'] = self.context.get('volatility')
        return super().create(validated_data)

# 포트폴리오 Serializer
class PortfolioSerializer(serializers.ModelSerializer):
    recommendation_logs = RecommendationLogSerializer(many=True, read_only=True)
    stocks = StockSerializer(many=True, read_only=True)  # 포트폴리오 내 주식 목록
    cryptocurrencies = CryptoSerializer(many=True, read_only=True)  # 포트폴리오 내 암호화폐 목록
    deposits = PortfolioDepositSerializer(source="portfolio_deposits", many=True, read_only=True)  # 예금 목록
    savings = PortfolioSavingSerializer(source="portfolio_savings", many=True, read_only=True)  # 적금 목록
    total_investment = serializers.DecimalField(
        max_digits=15, decimal_places=2, read_only=True  # 읽기 전용 필드
    )
    allocation = serializers.JSONField(read_only=True)  # 자산 비율 읽기 전용

    class Meta:
        model = Portfolio
        fields = [
            'id',
            'user',
            'name',
            'total_investment',
            'volatility',
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
            'user', 'created_at', 'updated_at', 'total_investment', 'volatility', 'allocation'
        ]

# 사용자 응답 Serializer
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['id', 'portfolio', 'current_step', 'responses']
