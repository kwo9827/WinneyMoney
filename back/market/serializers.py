from rest_framework import serializers
from .models import SearchIndex, SearchCoin

class SearchIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchIndex
        fields = ['name', 'ticker', 'market', 'currency']

class SearchCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchCoin
        fields = ['symbol',]