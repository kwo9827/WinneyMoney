from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Portfolio, Stock, Bond
from finlife.models import DepositProducts
from .serializers import PortfolioSerializer, StockSerializer, BondSerializer
from rest_framework.permissions import IsAuthenticated
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
@permission_classes([IsAuthenticated])
def portfolio_list_create(request):
    if request.method == 'GET':
        portfolios = Portfolio.objects.filter(user=request.user)
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PortfolioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        portfolio = serializer.save(user=request.user)
        total_investment = 0

        # 주식 및 채권 추가
        stocks_data = request.data.get("stocks", [])
        bonds_data = request.data.get("bonds", [])

        for stock_data in stocks_data:
            stock = create_stock(portfolio, stock_data)
            if stock:
                total_investment += stock.quantity * stock.purchase_price

        for bond_data in bonds_data:
            bond = create_bond(portfolio, bond_data)
            if bond:
                total_investment += bond.investment

        portfolio.total_investment = total_investment
        portfolio.save()

        response_data = recommend_savings_logic(portfolio)
        return Response(response_data, status=status.HTTP_201_CREATED)


# 포트폴리오 상세 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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


# 주식 추가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_stock(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    stocks_data = request.data.get("stocks", [])

    if not stocks_data:
        return Response({"error": "No stock data provided."}, status=status.HTTP_400_BAD_REQUEST)

    added_stocks = []
    errors = []
    for stock_data in stocks_data:
        try:
            stock = create_stock(portfolio, stock_data)
            if stock:
                added_stocks.append({
                    "ticker": stock.ticker,
                    "quantity": stock.quantity,
                    "purchase_price": stock.purchase_price,
                    "current_value": stock.current_value
                })
        except Exception as e:
            errors.append({"error": str(e), "stock_data": stock_data})

    if errors:
        return Response({"added_stocks": added_stocks, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"added_stocks": added_stocks}, status=status.HTTP_201_CREATED)


# 채권 추가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_bond(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    bonds_data = request.data.get("bonds", [])

    if not bonds_data:
        return Response({"error": "No bond data provided."}, status=status.HTTP_400_BAD_REQUEST)

    added_bonds = []
    errors = []
    for bond_data in bonds_data:
        try:
            bond = create_bond(portfolio, bond_data)
            if bond:
                added_bonds.append({
                    "name": bond.name,
                    "investment": bond.investment,
                    "yield_rate": bond.yield_rate,
                    "maturity_date": bond.maturity_date
                })
        except Exception as e:
            errors.append({"error": str(e), "bond_data": bond_data})

    if errors:
        return Response({"added_bonds": added_bonds, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"added_bonds": added_bonds}, status=status.HTTP_201_CREATED)


# 주식 생성 함수
def create_stock(portfolio, stock_data):
    try:
        stock_info = fdr.DataReader(stock_data["ticker"])
        current_price = stock_info.iloc[-1]["Close"]
        stock = Stock.objects.create(
            portfolio=portfolio,
            ticker=stock_data["ticker"],
            quantity=stock_data["quantity"],
            purchase_price=stock_data["purchase_price"],
            current_value=current_price,
        )
        return stock
    except Exception as e:
        return None


# 채권 생성 함수
def create_bond(portfolio, bond_data):
    try:
        bond = Bond.objects.create(
            portfolio=portfolio,
            name=bond_data["name"],
            investment=bond_data["investment"],
            yield_rate=bond_data["yield_rate"],
            maturity_date=bond_data.get("maturity_date"),
        )
        return bond
    except Exception as e:
        return None


# 추천 로직 호출
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_savings(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    response_data = recommend_savings_logic(portfolio)
    return Response(response_data)

# 주식 추가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_stock(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    stocks_data = request.data.get("stocks", [])

    if not stocks_data:
        return Response({"error": "No stock data provided."}, status=status.HTTP_400_BAD_REQUEST)

    added_stocks = []
    errors = []
    for stock_data in stocks_data:
        try:
            stock_info = fdr.DataReader(stock_data["ticker"])
            current_price = stock_info.iloc[-1]["Close"]
            stock = Stock.objects.create(
                portfolio=portfolio,
                ticker=stock_data["ticker"],
                quantity=stock_data["quantity"],
                purchase_price=stock_data["purchase_price"],
                current_value=current_price,
            )
            added_stocks.append({
                "ticker": stock.ticker,
                "quantity": stock.quantity,
                "purchase_price": stock.purchase_price,
                "current_value": stock.current_value,
            })
        except Exception as e:
            errors.append({"error": str(e), "stock_data": stock_data})

    if errors:
        return Response({"added_stocks": added_stocks, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"added_stocks": added_stocks}, status=status.HTTP_201_CREATED)


# 채권 추가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_bond(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    bonds_data = request.data.get("bonds", [])

    if not bonds_data:
        return Response({"error": "No bond data provided."}, status=status.HTTP_400_BAD_REQUEST)

    added_bonds = []
    errors = []
    for bond_data in bonds_data:
        try:
            bond = Bond.objects.create(
                portfolio=portfolio,
                name=bond_data["name"],
                investment=bond_data["investment"],
                yield_rate=bond_data["yield_rate"],
                maturity_date=bond_data.get("maturity_date"),
            )
            added_bonds.append({
                "name": bond.name,
                "investment": bond.investment,
                "yield_rate": bond.yield_rate,
                "maturity_date": bond.maturity_date,
            })
        except Exception as e:
            errors.append({"error": str(e), "bond_data": bond_data})

    if errors:
        return Response({"added_bonds": added_bonds, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"added_bonds": added_bonds}, status=status.HTTP_201_CREATED)
