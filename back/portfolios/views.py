from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Portfolio, Stock, Crypto
from finlife.models import DepositProducts, SavingProducts
from .serializers import PortfolioSerializer, StockSerializer, CryptoSerializer, RecommendationLogSerializer
from rest_framework.permissions import IsAuthenticated
import FinanceDataReader as fdr
import datetime

from .models import RecommendationLog
def recommend_products_logic(portfolio):
    try:
        # 포트폴리오 관련 변수 초기화
        predicted_economy = portfolio.predicted_economy
        risk_preference = portfolio.risk_preference

        total_investment = portfolio.total_investment
        stock_investment = sum(stock.purchase_price * stock.quantity for stock in portfolio.stocks.all())
        crypto_investment = sum(crypto.purchase_price * crypto.quantity for crypto in portfolio.cryptocurrencies.all())

        stock_ratio = stock_investment / total_investment if total_investment > 0 else 0
        crypto_ratio = crypto_investment / total_investment if total_investment > 0 else 0

        # 저장 상품(예금 및 적금) 가져오기
        deposits = DepositProducts.objects.prefetch_related("options").all()
        savings = SavingProducts.objects.prefetch_related("options").all()

        scored_products = []  # 추천 상품 리스트

        # 사용자 친화적인 메시지 작성
        portfolio_volatility_message = (
            f"고객님의 포트폴리오 변동성은 {portfolio.volatility or 'N/A'}입니다. "
            "변동성이 높을수록 수익률 변동이 크며, 공격적인 투자에 적합합니다. "
            "아래는 고객님의 투자 성향과 경제 예측에 기반한 추천 상품입니다."
        )

        # 예금 스코어 계산
        for deposit in deposits:
            score = 0
            reasons = []

            # 옵션 데이터가 없는 경우 생략
            if not deposit.options.exists():
                continue

            for option in deposit.options.all():
                score += option.intr_rate * 10
                reasons.append(f"기본 금리가 {option.intr_rate}%로 높습니다.")
                if predicted_economy == "growth" and option.save_trm >= 12:
                    score += 10
                    reasons.append("성장 경제에 적합한 장기 상품입니다.")
                elif predicted_economy == "recession" and option.save_trm < 12:
                    score += 5
                    reasons.append("하락 경제에 적합한 단기 상품입니다.")

                # 만기 후 혜택 반영
                if hasattr(option, "mtrt_int") and option.mtrt_int:
                    score += option.mtrt_int * 2
                    reasons.append(f"만기 후 이자율 {option.mtrt_int}%로 추가 혜택이 있습니다.")

            if risk_preference == "high" and crypto_ratio > 0.5:
                score += 10
                reasons.append("공격적인 투자 성향에 적합합니다.")
            elif risk_preference == "low" and stock_ratio > 0.6:
                score -= 10
                reasons.append("수비적인 투자 성향에 부적합합니다.")

            scored_products.append({
                "product": deposit,
                "score": score,
                "type": "deposit",
                "reasons": sorted(set(reasons), key=reasons.index)  # 중복 제거
            })

        # 적금 스코어 계산
        for saving in savings:
            score = 0
            reasons = []

            # 옵션 데이터가 없는 경우 생략
            if not saving.options.exists():
                continue

            for option in saving.options.all():
                score += option.intr_rate * 10
                reasons.append(f"기본 금리가 {option.intr_rate}%로 높습니다.")
                if predicted_economy == "growth" and option.save_trm >= 12:
                    score += 10
                    reasons.append("성장 경제에 적합한 장기 상품입니다.")
                elif predicted_economy == "recession" and option.save_trm < 12:
                    score += 5
                    reasons.append("하락 경제에 적합한 단기 상품입니다.")

                # 만기 후 혜택 반영
                if hasattr(option, "mtrt_int") and option.mtrt_int:
                    score += option.mtrt_int * 2
                    reasons.append(f"만기 후 이자율 {option.mtrt_int}%로 추가 혜택이 있습니다.")

            if risk_preference == "high" and crypto_ratio > 0.5:
                score += 10
                reasons.append("공격적인 투자 성향에 적합합니다.")
            elif risk_preference == "low" and stock_ratio > 0.6:
                score -= 10
                reasons.append("수비적인 투자 성향에 부적합합니다.")

            scored_products.append({
                "product": saving,
                "score": score,
                "type": "saving",
                "reasons": sorted(set(reasons), key=reasons.index)  # 중복 제거
            })

        # 스코어 기준 정렬
        scored_products.sort(key=lambda x: x["score"], reverse=True)

        # 추천 상품 저장 및 로그 생성
        for product in scored_products[:5]:  # 상위 5개만 추천
            content_type = ContentType.objects.get_for_model(product["product"].__class__)

            # 가장 높은 점수의 이유를 강조하여 표시
            main_reason = product["reasons"][0] if product["reasons"] else "추천 이유가 없습니다."

            # 추천 로그 중복 확인
            existing_log = RecommendationLog.objects.filter(
                portfolio=portfolio,
                content_type=content_type,
                object_id=product["product"].id
            ).first()

            recommendation_message = (
                f"{portfolio_volatility_message}\n\n"
                f"주요 이유: {main_reason}\n"
                f"추가 이유:\n" + "\n".join(product["reasons"])
            )

            if existing_log:
                # 이미 존재하는 경우, 추천 이유 업데이트
                existing_log.reason = recommendation_message
                existing_log.save()
            else:
                # 새로운 추천 로그 생성
                RecommendationLog.objects.create(
                    portfolio=portfolio,
                    content_type=content_type,
                    object_id=product["product"].id,
                    reason=recommendation_message,
                )

        return PortfolioSerializer(portfolio).data
    except Exception as e:
        return {"error": str(e)}


    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_products(request, portfolio_id):
    # 포트폴리오 가져오기
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    
    # 추천 로직 실행
    data = recommend_products_logic(portfolio)
    
    # 포트폴리오와 추천 로그 데이터를 분리하여 반환
    response_data = {
        "portfolio": PortfolioSerializer(portfolio).data,  # 포트폴리오 데이터
        "recommendations": RecommendationLogSerializer(
            portfolio.recommendation_logs.all(), many=True
        ).data  # 추천 로그 데이터
    }
    
    return Response(response_data)


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
        print(request.data)
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

            # 현재 날짜 및 6개월 전 계산
            purchase_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (pd.to_datetime(purchase_date) - pd.DateOffset(months=6)).strftime("%Y-%m-%d")

            # FinanceDataReader에서 데이터 가져오기
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
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    cryptos_data = request.data.get("cryptos", [])

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
    return Response({"added_cryptos": added_cryptos}, status=status.HTTP_201_CREATED)


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
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    stock = get_object_or_404(Stock, id=stock_id, portfolio=portfolio)
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
