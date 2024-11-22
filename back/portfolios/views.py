from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Portfolio, Stock, Bond
from finlife.models import DepositProducts
from .serializers import PortfolioSerializer, StockSerializer, BondSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes

import FinanceDataReader as fdr

# 추천 로직 함수
def recommend_savings_logic(portfolio):
    try:
        predicted_economy = portfolio.predicted_economy
        risk_preference = portfolio.risk_preference

        total_investment = portfolio.total_investment
        stock_investment = sum(stock.quantity * stock.purchase_price for stock in portfolio.stocks.all())
        bond_investment = sum(bond.investment for bond in portfolio.bonds.all())

        stock_ratio = stock_investment / total_investment if total_investment > 0 else 0
        bond_ratio = bond_investment / total_investment if total_investment > 0 else 0

        savings = DepositProducts.objects.all()
        scored_savings = []

        for saving in savings:
            score = 0
            for option in saving.depositoptions_set.all():
                score += option.intr_rate * 10
                if predicted_economy == "growth" and option.save_trm >= 12:
                    score += 10
                elif predicted_economy == "recession" and option.save_trm < 12:
                    score += 5
            if risk_preference == "high" and bond_ratio > 0.5:
                score += 10
            elif risk_preference == "low" and stock_ratio > 0.6:
                score -= 10
            scored_savings.append({"saving": saving, "score": score})

        scored_savings.sort(key=lambda x: x["score"], reverse=True)
        recommended_savings = [x["saving"] for x in scored_savings]
        portfolio.recommended_deposits.set(recommended_savings[:5])

        return PortfolioSerializer(portfolio).data
    except Exception as e:
        return {"error": str(e)}

# 포트폴리오 생성 및 목록 조회
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def portfolio_list_create(request):
    if request.method == 'GET':
        portfolios = Portfolio.objects.filter(user=request.user)
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid():
            portfolio = serializer.save(user=request.user)
            total_investment = 0

            # 주식 추가
            for stock_data in request.data.get("stocks", []):
                try:
                    stock_info = fdr.DataReader(stock_data["ticker"])
                    current_price = stock_info.iloc[-1]["Close"]
                    Stock.objects.create(
                        portfolio=portfolio,
                        ticker=stock_data["ticker"],
                        quantity=stock_data["quantity"],
                        purchase_price=stock_data["purchase_price"],
                        current_value=current_price
                    )
                    total_investment += stock_data["quantity"] * stock_data["purchase_price"]
                except Exception:
                    continue

            # 채권 추가
            for bond_data in request.data.get("bonds", []):
                Bond.objects.create(
                    portfolio=portfolio,
                    name=bond_data["name"],
                    investment=bond_data["investment"],
                    yield_rate=bond_data["yield_rate"]
                )
                total_investment += bond_data["investment"]

            portfolio.total_investment = total_investment
            portfolio.save()

            response_data = recommend_savings_logic(portfolio)
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 포트폴리오 상세 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)

    if request.method == 'GET':
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PortfolioSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            portfolio = serializer.save()
            response_data = recommend_savings_logic(portfolio)
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def add_or_update_stock(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)

    stocks_data = request.data.get("stocks", [])
    if not stocks_data:
        return Response({"error": "Stocks data is required"}, status=status.HTTP_400_BAD_REQUEST)

    errors = []
    for stock_data in stocks_data:
        serializer = StockSerializer(data=stock_data)
        if serializer.is_valid():
            serializer.save(portfolio=portfolio)
        else:
            errors.append(serializer.errors)

    if errors:
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    # 포트폴리오 총 투자 금액 재계산
    portfolio.save()

    return Response({"message": "Stocks updated successfully"}, status=status.HTTP_200_OK)

# 채권 추가
@api_view(['POST'])
def add_bond(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    serializer = BondSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(portfolio=portfolio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 추천 로직 호출
@api_view(['GET'])
def recommend_savings(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    response_data = recommend_savings_logic(portfolio)
    return Response(response_data)
