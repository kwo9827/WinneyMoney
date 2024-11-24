from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Portfolio, Stock, Crypto
from finlife.models import DepositProducts
from .serializers import PortfolioSerializer, StockSerializer, CryptoSerializer
from rest_framework.permissions import IsAuthenticated
import FinanceDataReader as fdr

# 추천 로직 함수
def recommend_savings_logic(portfolio):
    try:
        predicted_economy = portfolio.predicted_economy
        risk_preference = portfolio.risk_preference

        total_investment = portfolio.total_investment
        stock_investment = sum(stock.purchase_price * stock.quantity for stock in portfolio.stocks.all())
        crypto_investment = sum(crypto.purchase_price * crypto.quantity for crypto in portfolio.cryptocurrencies.all())

        stock_ratio = stock_investment / total_investment if total_investment > 0 else 0
        crypto_ratio = crypto_investment / total_investment if total_investment > 0 else 0

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
            if risk_preference == "high" and crypto_ratio > 0.5:
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
        if serializer.is_valid():
            portfolio = serializer.save(user=request.user)
            return Response(PortfolioSerializer(portfolio).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(PortfolioSerializer(portfolio).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from datetime import datetime
import pandas as pd
# 주식 추가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_stock(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    print(portfolio, '입력', request.data)
    stocks_data = request.data.get("stocks", [])
    print(stocks_data)

    if not stocks_data:
        return Response({"error": "No stock data provided."}, status=status.HTTP_400_BAD_REQUEST)

    added_stocks = []
    errors = []

    for stock_data in stocks_data:
        try:
            # 필수 입력 값 확인
            ticker = stock_data.get("ticker")
            purchase_price = stock_data.get("purchase_price")
            total_investment = stock_data.get("total_investment")

            if not ticker or not purchase_price or not total_investment:
                raise ValueError("Missing required stock data: ticker, purchase_price, or total_investment.")

            # 현재 날짜 및 6개월 전 계산
            purchase_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (pd.to_datetime(purchase_date) - pd.DateOffset(months=6)).strftime("%Y-%m-%d")

            # FinanceDataReader에서 데이터 가져오기
            stock_info = fdr.DataReader(ticker, start_date, purchase_date)
            print(stock_info)
            if stock_info.empty:
                raise ValueError(f"Ticker '{ticker}' not found or no data available.")

            # 현재 가격 및 변동성 계산
            current_price = stock_info.iloc[-1]["Close"]
            weekly_returns = stock_info["Close"].pct_change().dropna()
            print(weekly_returns)
            volatility = weekly_returns.std() * (126**0.5)  # 연간화된 변동성

            # 수량 계산
            quantity = total_investment / purchase_price

            # Stock 객체 생성
            stock = Stock.objects.create(
                portfolio=portfolio,
                ticker=ticker,
                purchase_price=purchase_price,
                total_investment=total_investment,
                quantity=quantity,
                current_value=current_price,
                volatility=volatility,
            )
            added_stocks.append(StockSerializer(stock).data)

        except ValueError as ve:
            # 데이터 입력 오류 처리
            errors.append({"error": str(ve), "stock_data": stock_data})
        except Exception as e:
            # 일반적인 예외 처리
            errors.append({"error": "An unexpected error occurred: " + str(e), "stock_data": stock_data})

    if errors:
        return Response({"added_stocks": added_stocks, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"added_stocks": added_stocks}, status=status.HTTP_201_CREATED)


# 암호화폐 추가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_crypto(request, portfolio_id):
    print(request.data)
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    print(portfolio)
    cryptos_data = request.data.get("cryptos", [])
    print(cryptos_data)
    if not cryptos_data:
        return Response({"error": "No cryptocurrency data provided."}, status=status.HTTP_400_BAD_REQUEST)

    added_cryptos = []
    errors = []

    for crypto_data in cryptos_data:
        try:
            # 필수 데이터 확인
            print(crypto_data)
            symbol = crypto_data.get("symbol")
            purchase_price = crypto_data.get("purchase_price")
            total_investment = crypto_data.get("total_investment")

            if not symbol or not purchase_price or not total_investment:
                raise ValueError("Missing required cryptocurrency data: symbol, purchase_price, or total_investment.")

            # 구매일 및 6개월 전 데이터 설정
            purchase_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (pd.to_datetime(purchase_date) - pd.DateOffset(months=6)).strftime("%Y-%m-%d")

            # FinanceDataReader에서 데이터 가져오기
            try:
                crypto_info = fdr.DataReader(f"{symbol}/KRW", start_date, purchase_date)
                if crypto_info.empty:
                    raise ValueError(f"Symbol '{symbol}' not found or no data available.")
            except Exception:
                raise ValueError(f"Failed to retrieve data for symbol '{symbol}'. Please check the symbol.")

            # 현재 가격 및 변동성 계산
            current_price = crypto_info.iloc[-1]["Close"]
            weekly_returns = crypto_info["Close"].pct_change().dropna()
            volatility = weekly_returns.std() * (126**0.5)  # 연간화된 변동성

            # 수량 계산
            quantity = total_investment / purchase_price

            # Crypto 객체 생성
            crypto = Crypto.objects.create(
                portfolio=portfolio,
                symbol=symbol,
                name=crypto_data.get("name", "Unknown"),
                purchase_price=purchase_price,
                total_investment=total_investment,
                quantity=quantity,
                current_value=current_price,
                volatility=volatility,
            )
            added_cryptos.append(CryptoSerializer(crypto).data)

        except ValueError as ve:
            # 데이터 입력 오류 처리
            errors.append({"error": str(ve), "crypto_data": crypto_data})
        except Exception as e:
            # 일반적인 예외 처리
            errors.append({"error": "An unexpected error occurred: " + str(e), "crypto_data": crypto_data})

    if errors:
        return Response({"added_cryptos": added_cryptos, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)
    print(added_cryptos)
    return Response({"added_cryptos": added_cryptos}, status=status.HTTP_201_CREATED)

# 추천 로직 호출
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_savings(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    response_data = recommend_savings_logic(portfolio)
    return Response(response_data)

# 주식 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_stock(request, portfolio_id, stock_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    stock = get_object_or_404(Stock, id=stock_id, portfolio=portfolio)

    stock.delete()
    return Response({"message": "Stock deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# 암호화폐 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_crypto(request, portfolio_id, crypto_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    crypto = get_object_or_404(Crypto, id=crypto_id, portfolio=portfolio)

    crypto.delete()
    return Response({"message": "Cryptocurrency deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# 주식 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_stock(request, portfolio_id, stock_id):
    print('응답')
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    print(portfolio)
    stock = get_object_or_404(Stock, id=stock_id, portfolio=portfolio)
    print(stock)

    print(portfolio, stock)
    serializer = StockSerializer(stock, data=request.data, partial=True)
    if serializer.is_valid():
        stock = serializer.save()
        return Response(StockSerializer(stock).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 암호화폐 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_crypto(request, portfolio_id, crypto_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    crypto = get_object_or_404(Crypto, id=crypto_id, portfolio=portfolio)

    serializer = CryptoSerializer(crypto, data=request.data, partial=True)
    if serializer.is_valid():
        crypto = serializer.save()
        return Response(CryptoSerializer(crypto).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
