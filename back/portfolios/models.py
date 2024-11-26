from django.db import models
from django.conf import settings
from finlife.models import DepositProducts, SavingProducts

User = settings.AUTH_USER_MODEL

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolios")
    name = models.CharField(max_length=100)

    # 사용자 입력 값
    current_cash = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    monthly_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
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
    total_investment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_volatility = models.FloatField(null=True, blank=True)
    allocation = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total_investment(self):
        """
        포트폴리오의 총 자산 계산.
        """
        stock_total = sum([stock.current_investment for stock in self.stocks.all()])
        crypto_total = sum([crypto.current_investment for crypto in self.cryptocurrencies.all()])
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
        stock_total = sum([stock.current_investment for stock in self.stocks.all()])
        crypto_total = sum([crypto.current_investment for crypto in self.cryptocurrencies.all()])
        deposit_total = sum([deposit.balance for deposit in self.portfolio_deposits.all()])
        saving_total = sum([saving.balance for saving in self.portfolio_savings.all()])
        total = stock_total + crypto_total + deposit_total + saving_total + self.current_cash

        if total > 0:
            return {
                "stock": float((stock_total / total) * 100),
                "crypto": float((crypto_total / total) * 100),
                "deposit": float((deposit_total / total) * 100),
                "saving": float((saving_total / total) * 100),
                "cash": float((self.current_cash / total) * 100),
            }
        return {"stock": 0.0, "crypto": 0.0, "deposit": 0.0, "saving": 0.0, "cash": 0.0}

    def save(self, *args, **kwargs):
        # 객체가 이미 저장된 경우에만 계산
        super().save(*args, **kwargs)

        # 관계 필드를 사용한 계산을 위해 다시 저장
        self.total_investment = self.calculate_total_investment()
        self.total_volatility = self.calculate_total_volatility()
        self.allocation = self.calculate_allocation()

        # 다시 저장하여 계산된 값을 반영
        super().save(update_fields=['total_investment', 'total_volatility', 'allocation'])

    def __str__(self):
        return f"{self.user.username}'s Portfolio: {self.name}"


class Stock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="stocks")
    ticker = models.CharField(max_length=10)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2)
    total_investment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    quantity = models.DecimalField(max_digits=15, decimal_places=6, editable=False)  # 자동 계산
    current_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    current_investment = models.DecimalField(max_digits=15, decimal_places=2, editable=False, default=0)  # 현재 총 투자 금액
    volatility = models.FloatField(null=True, blank=True)  # 변동성 추가
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_quantity(self):
        return self.total_investment / self.purchase_price
    
    def calculate_current_investment(self):
        """
        현재 총 투자 금액: 수량 * 현재가
        """
        return self.quantity * self.current_value

    def save(self, *args, **kwargs):
        self.quantity = self.calculate_quantity()
        self.current_investment = self.calculate_current_investment()
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
    current_investment = models.DecimalField(max_digits=15, decimal_places=2, editable=False, default=0)  # 현재 총 투자 금액
    volatility = models.FloatField(null=True, blank=True)  # 변동성 추가
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_quantity(self):
        return self.total_investment / self.purchase_price
    
    def calculate_current_investment(self):
        """
        현재 총 투자 금액: 수량 * 현재가
        """
        return self.quantity * self.current_value

    def save(self, *args, **kwargs):
        self.quantity = self.calculate_quantity()
        self.current_investment = self.calculate_current_investment()
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

    recommended_volatility = models.FloatField(blank=True, null=True)  # 추천 후 변동성 추가
    recommended_allocation = models.JSONField(default=dict, blank=True)  # 추천 비율 저장
    recommended_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  # 추천 금액
    reason = models.TextField(blank=True, null=True)  # 추천 이유
    created_at = models.DateTimeField(auto_now_add=True)  # 추천 생성일

    def __str__(self):
        return f"Recommendation for {self.portfolio.name}: {self.product}"

    class Meta:
        ordering = ["-created_at"]  # 최신 로그가 먼저 나오도록 정렬

