from rest_framework import serializers
from .models import Portfolio, Stock, Crypto, UserResponse, RecommendationLog

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
        stock = Stock.objects.create(**validated_data)
        # 변동성 계산 후 저장 (뷰에서 추가 처리 가능)
        stock.volatility = self.context.get('volatility', None)
        stock.save()
        return stock


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
        crypto = Crypto.objects.create(**validated_data)
        # 변동성 계산 후 저장 (뷰에서 추가 처리 가능)
        crypto.volatility = self.context.get('volatility', None)
        crypto.save()
        return crypto


# 포트폴리오 Serializer
class PortfolioSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True, read_only=True)  # 포트폴리오 내 주식 목록
    cryptocurrencies = CryptoSerializer(many=True, read_only=True)  # 포트폴리오 내 암호화폐 목록
    total_investment = serializers.DecimalField(
        max_digits=15, decimal_places=2, read_only=True  # 읽기 전용 필드
    )

    class Meta:
        model = Portfolio
        fields = [
            'id',
            'user',
            'name',
            'total_investment',
            'predicted_economy',
            'risk_preference',
            'stocks',
            'cryptocurrencies',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


# 사용자 응답 Serializer
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['id', 'portfolio', 'current_step', 'responses']


# 추천 로그 Serializer
class RecommendationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationLog
        fields = ['id', 'portfolio', 'product', 'reason', 'created_at']
