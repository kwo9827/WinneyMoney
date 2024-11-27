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
        # 포트폴리오 정보 초기화
        predicted_economy = portfolio.predicted_economy
        risk_preference = portfolio.risk_preference
        current_volatility = float(portfolio.total_volatility)
        current_cash = float(portfolio.current_cash)
        monthly_income = float(portfolio.monthly_income)
        total_investment = float(portfolio.total_investment)

        # 1. 시장 상황에 따른 기본 비율 설정
        target_allocation = {"investment": 40, "saving": 60}
        if predicted_economy == "growth":
            target_allocation.update({"investment": 60, "saving": 40})
        elif predicted_economy == "recession":
            target_allocation.update({"investment": 30, "saving": 70})

        # 2. 투자 성향에 따른 비율 조정
        if risk_preference == "low":
            target_allocation["investment"] -= 10
            target_allocation["saving"] += 10
        elif risk_preference == "high":
            target_allocation["investment"] += 10
            target_allocation["saving"] -= 10

        # 3. 변동성에 따른 내부 분배
        if current_volatility < 0.2:
            investment_allocation = {
                "stock": target_allocation["investment"] * 0.8,
                "crypto": target_allocation["investment"] * 0.2,
            }
            saving_allocation = {
                "deposit": target_allocation["saving"] * 0.2,
                "saving": target_allocation["saving"] * 0.8,
            }
        elif 0.2 <= current_volatility <= 0.5:
            investment_allocation = {
                "stock": target_allocation["investment"] * 0.6,
                "crypto": target_allocation["investment"] * 0.4,
            }
            saving_allocation = {
                "deposit": target_allocation["saving"] * 0.4,
                "saving": target_allocation["saving"] * 0.6,
            }
        else:  # High volatility
            investment_allocation = {
                "stock": target_allocation["investment"] * 0.4,
                "crypto": target_allocation["investment"] * 0.6,
            }
            saving_allocation = {
                "deposit": target_allocation["saving"] * 0.6,
                "saving": target_allocation["saving"] * 0.4,
            }

        # 4. 가용 현금에 따른 비율 조정
        if current_cash < total_investment * 0.1:
            target_allocation["cash"] = 15
            target_allocation["investment"] -= 5
        else:
            target_allocation["cash"] = 5
            target_allocation["investment"] += 5

        # 5. 월 수입에 따른 비율 조정
        if monthly_income > 3000000:
            target_allocation["saving"] += 10
            target_allocation["investment"] -= 10
        elif monthly_income < 1000000:
            target_allocation["saving"] -= 10
            target_allocation["investment"] += 10

        # 변동성 계산 함수
        def calculate_volatility(portfolio, investment_allocation, saving_allocation, cash_allocation):
            stock_volatility = sum(
                stock.volatility * (investment_allocation.get("stock", 0) / 100)
                for stock in portfolio.stocks.all()
                if stock.volatility is not None
            )
            crypto_volatility = sum(
                crypto.volatility * (investment_allocation.get("crypto", 0) / 100)
                for crypto in portfolio.cryptocurrencies.all()
                if crypto.volatility is not None
            )
            # 예금 및 적금의 안정성은 변동성 없음으로 가정
            saving_volatility = saving_allocation.get("saving", 0) * 0
            deposit_volatility = saving_allocation.get("deposit", 0) * 0
            # 현금의 안정성은 변동성 없음으로 가정
            cash_volatility = cash_allocation * 0

            # 총 변동성 (가중 평균)
            total_volatility = stock_volatility + crypto_volatility + saving_volatility + deposit_volatility + cash_volatility
            return round(total_volatility, 4)

        # 추천 후 변동성 계산
        recommended_volatility = calculate_volatility(
            portfolio,
            investment_allocation,
            saving_allocation,
            target_allocation["cash"]
        )

        # 예금 및 적금 추천
        deposits = DepositProducts.objects.prefetch_related("options").all()
        savings = SavingProducts.objects.prefetch_related("options").all()

        def allocate_and_recommend(product_set, total_amount, product_type, max_recommendations=3):
            """
            상품 추천 및 투자 금액 계산
            """
            scored_products = []
            for product in product_set:
                if not product.options.exists():
                    continue
                score = 0
                reasons = []
                for option in product.options.all():
                    score += option.intr_rate * 10
                    reasons.append(f"기본 금리가 {option.intr_rate}%로 높습니다.")
                    if predicted_economy == "growth" and option.save_trm >= 12:
                        score += 10
                        reasons.append("성장 경제에 적합한 장기 상품입니다.")
                    elif predicted_economy == "recession" and option.save_trm < 12:
                        score += 5
                        reasons.append("불황 경제에 적합한 단기 상품입니다.")
                scored_products.append({
                    "product": product,
                    "score": score,
                    "reasons": reasons,
                })

            # 스코어 정렬 및 추천 상품 계산
            scored_products.sort(key=lambda x: x["score"], reverse=True)
            recommendations = []
            for product_data in scored_products[:max_recommendations]:
                if total_amount <= 0:
                    break
                recommended_amount = min(product_data["product"].max_limit or total_amount, total_amount)
                recommendations.append({
                    "product_name": product_data["product"].fin_prdt_nm,
                    "product_type": product_type.capitalize(),
                    "recommended_amount": recommended_amount,
                    "reason": " | ".join(product_data["reasons"]),
                })
                # RecommendationLog 저장
                RecommendationLog.objects.update_or_create(
                    portfolio=portfolio,
                    content_type=ContentType.objects.get_for_model(product_data["product"].__class__),
                    object_id=product_data["product"].id,
                    reason=" | ".join(product_data["reasons"]),
                    recommended_allocation={product_type: total_amount},
                    recommended_amount=recommended_amount,
                    recommended_volatility=recommended_volatility,  # 저장
                )
                total_amount -= recommended_amount

            return recommendations

        deposit_recommendations = allocate_and_recommend(
            deposits, total_investment * (saving_allocation["deposit"] / 100), "deposit"
        )
        saving_recommendations = allocate_and_recommend(
            savings, total_investment * (saving_allocation["saving"] / 100), "saving"
        )

        # 최종 응답 데이터 생성
        return {
            "current_allocation": portfolio.allocation,
            "recommended_allocation": {
                "investment": target_allocation["investment"],
                "saving": target_allocation["saving"],
                "cash": target_allocation["cash"],
            },
            "current_volatility": current_volatility,
            "recommended_volatility": recommended_volatility,
            "investment_allocation": investment_allocation,
            "saving_allocation": saving_allocation,
            "recommendations": deposit_recommendations + saving_recommendations,
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

    # PortfolioSerializer로 직렬화
    serialized_portfolio = PortfolioSerializer(portfolio).data

    # RecommendationLog에서 현재 포트폴리오의 추천 로그 가져오기
    recommendation_logs = RecommendationLog.objects.filter(portfolio=portfolio)
    serialized_logs = RecommendationLogSerializer(recommendation_logs, many=True).data

    # 응답 데이터 구성
    response_data = {
        "portfolio": serialized_portfolio,
        "investment_allocation": recommendation_data.get("investment_allocation"),
        "saving_allocation": recommendation_data.get("saving_allocation"),
        "recommendations": serialized_logs,
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

