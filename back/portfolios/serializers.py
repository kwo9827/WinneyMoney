from rest_framework import serializers
from .models import Portfolio, Stock, Bond

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
        read_only_fields = ['portfolio']  # portfolio는 자동으로 설정

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = '__all__'
        read_only_fields = ['portfolio']  # portfolio는 자동으로 설정
        
class PortfolioSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True, read_only=True)  # 연결된 주식 정보
    bonds = BondSerializer(many=True, read_only=True)    # 연결된 채권 정보

    class Meta:
        model = Portfolio
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')