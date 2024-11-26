from django.db import models
from django.conf import settings
from finlife.models import DepositProducts, SavingProducts

User = settings.AUTH_USER_MODEL

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolios")
    name = models.CharField(max_length=100)

    # 사용자 입력 값
    current_cash = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # 즉시 가용 자산
    monthly_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # 월 평균 수입
    predicted_economy = models.CharField(
        max_length=100,
        choices=[('recession', '하락'), ('growth', '성장'), ('stability', '유지')],
        blank=True,
        null=True
    )
    risk_preference = models.CharField(
        max_length=100,
        choices=[('low', '수비적'), ('medium', '보통'), ('high', '공격형')],
        blank=True,
        null=True
    )

    # 자동 계산 값
    total_investment = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # 총 자산
    total_volatility = models.FloatField(null=True, blank=True)  # 포트폴리오 총 변동성
    allocation = models.JSONField(default=dict, blank=True)  # 실제 보유 비율

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_investment(self):
        """
        포트폴리오의 총 자산 계산.
        """
        stock_total = sum([stock.total_investment for stock in self.stocks.all()])
        crypto_total = sum([crypto.total_investment for crypto in self.cryptocurrencies.all()])
        deposit_total = sum([deposit.balance for deposit in self.portfolio_deposits.all()])
        saving_total = sum([saving.balance for saving in self.portfolio_savings.all()])

        return stock_total + crypto_total + deposit_total + saving_total + self.current_cash

    def calculate_total_volatility(self):
        """
        주식과 암호화폐의 변동성을 기반으로 포트폴리오 총 변동성 계산.
        """
        stock_volatility = [stock.volatility for stock in self.stocks.all() if stock.volatility is not None]
        crypto_volatility = [crypto.volatility for crypto in self.cryptocurrencies.all() if crypto.volatility is not None]
        all_volatility = stock_volatility + crypto_volatility

        if all_volatility:
            return sum(all_volatility) / len(all_volatility)
        return 0

    def calculate_allocation(self):
        """
        실제 보유 자산 비율 계산.
        """
        stock_total = sum([stock.total_investment for stock in self.stocks.all()])
        crypto_total = sum([crypto.total_investment for crypto in self.cryptocurrencies.all()])
        deposit_total = sum([deposit.balance for deposit in self.portfolio_deposits.all()])
        saving_total = sum([saving.balance for saving in self.portfolio_savings.all()])
        total = stock_total + crypto_total + deposit_total + saving_total + self.current_cash

        if total > 0:
            return {
                "stock": round((stock_total / total) * 100, 2),
                "crypto": round((crypto_total / total) * 100, 2),
                "deposit": round((deposit_total / total) * 100, 2),
                "saving": round((saving_total / total) * 100, 2),
                "cash": round((self.current_cash / total) * 100, 2),
            }
        return {"stock": 0.0, "crypto": 0.0, "deposit": 0.0, "saving": 0.0, "cash": 0.0}

    def save(self, *args, **kwargs):
        # 자동 계산 값 업데이트
        self.total_investment = self.calculate_total_investment()
        self.allocation = self.calculate_allocation()
        self.total_volatility = self.calculate_total_volatility()

        # 객체를 데이터베이스에 저장
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Portfolio: {self.name}"


class Stock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="stocks")
    ticker = models.CharField(max_length=10)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2)
    total_investment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    quantity = models.DecimalField(max_digits=15, decimal_places=6, editable=False)  # 자동 계산
    current_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    volatility = models.FloatField(null=True, blank=True)  # 변동성 추가
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_quantity(self):
        return self.total_investment / self.purchase_price

    def save(self, *args, **kwargs):
        self.quantity = self.calculate_quantity()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticker} in {self.portfolio.name}"


class Crypto(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="cryptocurrencies")
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2)
    total_investment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    quantity = models.DecimalField(max_digits=15, decimal_places=6, editable=False)  # 자동 계산
    current_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    volatility = models.FloatField(null=True, blank=True)  # 변동성 추가
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_quantity(self):
        return self.total_investment / self.purchase_price

    def save(self, *args, **kwargs):
        self.quantity = self.calculate_quantity()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.symbol}) in {self.portfolio.name}"


class PortfolioDeposit(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="portfolio_deposits")
    deposit_product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name="portfolio_deposits")
    balance = models.DecimalField(max_digits=15, decimal_places=2)  # 가입 금액
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.portfolio.name} - {self.deposit_product.fin_prdt_nm}"


class PortfolioSaving(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="portfolio_savings")
    saving_product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE, related_name="portfolio_savings")
    balance = models.DecimalField(max_digits=15, decimal_places=2)  # 가입 금액
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.portfolio.name} - {self.saving_product.fin_prdt_nm}"



class UserResponse(models.Model):
    portfolio = models.OneToOneField(Portfolio, on_delete=models.CASCADE, related_name="user_response")
    current_step = models.PositiveIntegerField(default=0)  # 사용자가 어디까지 응답했는지 저장
    responses = models.JSONField(default=dict)  # 각 단계별 응답 데이터를 저장

    def __str__(self):
        return f"Responses for {self.portfolio.name}"


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class RecommendationLog(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="recommendation_logs")

    # 다형성 지원을 위한 필드
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 추천 상품의 모델 타입
    object_id = models.PositiveIntegerField()  # 추천 상품의 ID
    product = GenericForeignKey("content_type", "object_id")  # 실제 추천 상품

    reason = models.TextField(blank=True, null=True)  # 추천 이유
    created_at = models.DateTimeField(auto_now_add=True)  # 추천 생성일

    def __str__(self):
        return f"Recommendation for {self.portfolio.name}: {self.product}"

    class Meta:
        ordering = ["-created_at"]  # 최신 로그가 먼저 나오도록 정렬

