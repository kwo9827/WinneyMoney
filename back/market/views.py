from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  # Q 객체 import

from .models import SearchIndex, SearchCoin
from .serializers import SearchIndexSerializer, SearchCoinSerializer

@api_view(['GET'])
def search(request):
    query = request.GET.get('query', '').strip()
    if not query:
        return Response({"error": "검색어를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
    print(query)
    # 이름(name)과 Ticker 동시 검색
    results = SearchIndex.objects.filter(
        Q(name__icontains=query) | Q(ticker__icontains=query)
    )[:3]  # 상위 10개 결과만 반환

    # 데이터 직렬화 및 응답 반환
    serializer = SearchIndexSerializer(results, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def search_coin(request):
    print(request)
    query = request.GET.get('query', '').strip()
    print(query)
    if not query:
        return Response({"error": "검색어를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
    print(query)
    results = SearchCoin.objects.filter(
        Q(symbol__icontains=query)
    )[:3]  # 상위 10개 결과만 반환

    print(results)
    # 데이터 직렬화 및 응답 반환
    serializer = SearchCoinSerializer(results, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
