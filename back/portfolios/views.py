from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Portfolio, Stock, Crypto, PortfolioDeposit, PortfolioSaving, RecommendationLog
)
from finlife.models import DepositProducts, SavingProducts
from .serializers import (
    PortfolioSerializer, StockSerializer, CryptoSerializer,
    RecommendationLogSerializer, PortfolioDepositSerializer, PortfolioSavingSerializer
)
from rest_framework.permissions import IsAuthenticated
import FinanceDataReader as fdr
from datetime import datetime
import pandas as pd

from .models import RecommendationLog
def recommend_products_logic(portfolio):
    try:
        # 포트폴리오 관련 변수 초기화
        predicted_economy = portfolio.predicted_economy
        risk_preference = portfolio.risk_preference
        volatility = portfolio.total_volatility
        current_allocation = portfolio.allocation
        current_cash = portfolio.current_cash
        monthly_income = portfolio.monthly_income

        # 기본 추천 비율 설정
        if predicted_economy == "growth":
            target_allocation = {"investment": 60, "saving": 40}
        elif predicted_economy == "recession":
            target_allocation = {"investment": 30, "saving": 70}
        else:  # stability
            target_allocation = {"investment": 40, "saving": 60}

        # risk_preference 반영
        if risk_preference == "low":  # 수비적
            target_allocation["investment"] -= 10
            target_allocation["saving"] += 10
        elif risk_preference == "high":  # 공격적
            target_allocation["investment"] += 10
            target_allocation["saving"] -= 10

        # 현금 비중 조정
        if current_cash < portfolio.total_investment * 0.1:
            target_allocation["cash"] = 15  # 현금이 적을 경우 비율 증가
            target_allocation["investment"] -= 5  # 투자 비중 감소
        else:
            target_allocation["cash"] = 5  # 현금이 충분하면 비율 감소
            target_allocation["investment"] += 5  # 투자 비중 증가

        # 월 수입 비중 조정
        if monthly_income > 3000000:  # 월 수입이 충분한 경우 적금 증가
            target_allocation["saving"] += 10
            target_allocation["investment"] -= 10
        elif monthly_income < 1000000:  # 월 수입이 적은 경우 예금 증가
            target_allocation["saving"] -= 10
            target_allocation["investment"] += 10

        # 투자자산 내부 비율
        investment_allocation = {
            "stock": target_allocation["investment"] * (1 - volatility),
            "crypto": target_allocation["investment"] * volatility,
        }

        # 예/적금 내부 비율
        saving_allocation = {
            "deposit": target_allocation["saving"] * volatility,
            "saving": target_allocation["saving"] * (1 - volatility),
        }

        # 현재와 추천 비율 비교 메시지 생성
        adjustment_message = f"""
        현재 포트폴리오 비율은 다음과 같습니다:
        - 주식: {current_allocation.get('stock', 0)}%
        - 암호화폐: {current_allocation.get('crypto', 0)}%
        - 예금: {current_allocation.get('deposit', 0)}%
        - 적금: {current_allocation.get('saving', 0)}%
        - 현금: {current_allocation.get('cash', 0)}%

        추천 비율:
        - 주식: {investment_allocation['stock']}%
        - 암호화폐: {investment_allocation['crypto']}%
        - 예금: {saving_allocation['deposit']}%
        - 적금: {saving_allocation['saving']}%
        - 현금: {target_allocation.get('cash', 10)}%

        변동성({volatility:.2f})과 시장 상황({predicted_economy}), 투자 성향({risk_preference}), 
        현금({current_cash}), 월 수입({monthly_income})을 고려하여 비율을 조정하는 것을 권장합니다.
        """

        # 저장 상품(예금 및 적금) 가져오기
        deposits = DepositProducts.objects.prefetch_related("options").all()
        savings = SavingProducts.objects.prefetch_related("options").all()

        scored_products = []

        # 예금 및 적금 상품 점수 계산
        for product_set, product_type, allocation_key in [
            (deposits, "deposit", "deposit"),
            (savings, "saving", "saving"),
        ]:
            for product in product_set:
                score = 0
                reasons = []

                if not product.options.exists():
                    continue

                for option in product.options.all():
                    score += option.intr_rate * 10
                    reasons.append(f"기본 금리가 {option.intr_rate}%로 높습니다.")
                    if predicted_economy == "growth" and option.save_trm >= 12:
                        score += 10
                        reasons.append("성장 경제에 적합한 장기 상품입니다.")
                    elif predicted_economy == "recession" and option.save_trm < 12:
                        score += 5
                        reasons.append("하락 경제에 적합한 단기 상품입니다.")

                scored_products.append({
                    "product": product,
                    "type": product_type,
                    "score": score,
                    "reasons": reasons,
                    "recommended_amount": portfolio.total_investment * (saving_allocation[allocation_key] / 100),
                })

        # 스코어 기준 정렬
        scored_products.sort(key=lambda x: x["score"], reverse=True)

        # 추천 상품 생성
        recommendations = []
        for product_data in scored_products[:5]:  # 상위 5개 상품만 포함
            recommendations.append({
                "product_name": product_data["product"].fin_prdt_nm,
                "product_type": product_data["type"],
                "recommended_amount": product_data["recommended_amount"],
                "reason": " | ".join(product_data["reasons"]),
            })

        return {
            "portfolio": PortfolioSerializer(portfolio).data,
            "adjustment_message": adjustment_message.strip(),
            "recommendations": recommendations,
        }
    except Exception as e:
        return {"error": str(e)}




    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_products(request, portfolio_id):
    """
    포트폴리오를 기반으로 비율 조정 및 상품 추천 데이터를 반환합니다.
    """
    # 포트폴리오 가져오기
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)

    # 추천 로직 실행
    recommendation_data = recommend_products_logic(portfolio)

    # 추천 로직에서 에러가 반환된 경우 처리
    if "error" in recommendation_data:
        return Response({"error": recommendation_data["error"]}, status=status.HTTP_400_BAD_REQUEST)

    # 응답 데이터 구성
    response_data = {
        "portfolio": recommendation_data.get("portfolio"),  # 포트폴리오 데이터
        "adjustment_message": recommendation_data.get("adjustment_message"),  # 비율 조정 메시지
        "recommendations": recommendation_data.get("recommendations"),  # 추천 상품 리스트
    }

    return Response(response_data, status=status.HTTP_200_OK)



# --- Portfolio Views ---
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def portfolio_list_create(request):
    if request.method == 'GET':
        portfolios = Portfolio.objects.filter(user=request.user)
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PortfolioSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            portfolio = serializer.save(user=request.user)
            return Response(PortfolioSerializer(portfolio).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

# --- Stock Views ---
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
            # 필수 입력 값 확인
            ticker = stock_data.get("ticker")
            purchase_price = stock_data.get("purchase_price")
            total_investment = stock_data.get("total_investment")

            if not ticker or not purchase_price or not total_investment:
                raise ValueError("Missing required stock data: ticker, purchase_price, or total_investment.")

            # FinanceDataReader에서 데이터 가져오기
            purchase_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (pd.to_datetime(purchase_date) - pd.DateOffset(months=6)).strftime("%Y-%m-%d")
            stock_info = fdr.DataReader(ticker, start_date, purchase_date)

            if stock_info.empty:
                raise ValueError(f"Ticker '{ticker}' not found or no data available.")

            # 현재 가격 및 변동성 계산
            current_price = stock_info.iloc[-1]["Close"]
            weekly_returns = stock_info["Close"].pct_change().dropna()
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
            errors.append({"error": str(ve), "stock_data": stock_data})
        except Exception as e:
            errors.append({"error": f"An unexpected error occurred: {str(e)}", "stock_data": stock_data})

    if errors:
        return Response({"added_stocks": added_stocks, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"added_stocks": added_stocks}, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_stock(request, portfolio_id, stock_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    stock = get_object_or_404(Stock, id=stock_id, portfolio=portfolio)

    serializer = StockSerializer(stock, data=request.data, partial=True)
    if serializer.is_valid():
        stock = serializer.save()
        return Response(StockSerializer(stock).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_stock(request, portfolio_id, stock_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    stock = get_object_or_404(Stock, id=stock_id, portfolio=portfolio)
    stock.delete()
    return Response({"message": "Stock deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# --- Crypto Views ---
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_crypto(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    cryptos_data = request.data.get("cryptos", [])

    if not cryptos_data:
        return Response({"error": "No cryptocurrency data provided."}, status=status.HTTP_400_BAD_REQUEST)

    added_cryptos = []
    errors = []

    for crypto_data in cryptos_data:
        try:
            # 필수 데이터 확인
            symbol = crypto_data.get("symbol")
            purchase_price = crypto_data.get("purchase_price")
            total_investment = crypto_data.get("total_investment")

            if not symbol or not purchase_price or not total_investment:
                raise ValueError("Missing required cryptocurrency data: symbol, purchase_price, or total_investment.")

            # FinanceDataReader에서 데이터 가져오기
            purchase_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (pd.to_datetime(purchase_date) - pd.DateOffset(months=6)).strftime("%Y-%m-%d")
            crypto_info = fdr.DataReader(f"{symbol}/KRW", start_date, purchase_date)

            if crypto_info.empty:
                raise ValueError(f"Symbol '{symbol}' not found or no data available.")

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
            errors.append({"error": str(ve), "crypto_data": crypto_data})
        except Exception as e:
            errors.append({"error": f"An unexpected error occurred: {str(e)}", "crypto_data": crypto_data})

    if errors:
        return Response({"added_cryptos": added_cryptos, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"added_cryptos": added_cryptos}, status=status.HTTP_201_CREATED)

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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_crypto(request, portfolio_id, crypto_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    crypto = get_object_or_404(Crypto, id=crypto_id, portfolio=portfolio)
    crypto.delete()
    return Response({"message": "Cryptocurrency deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

