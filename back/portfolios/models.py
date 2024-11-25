from django.db import models
from django.conf import settings
from finlife.models import DepositProducts, SavingProducts
from datetime import date

User = settings.AUTH_USER_MODEL

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolios")
    name = models.CharField(max_length=100)
    total_investment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    volatility = models.FloatField(null=True, blank=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    recommended_deposits = models.ManyToManyField(DepositProducts, related_name="recommended_to_portfolios", blank=True)
    recommended_savings = models.ManyToManyField(SavingProducts, related_name="recommended_to_portfolios", blank=True)

    def calculate_total_investment(self):
        stock_investment = sum([
            stock.total_investment for stock in self.stocks.all()
        ]) if self.pk else 0

        crypto_investment = sum([
            crypto.total_investment for crypto in self.cryptocurrencies.all()
        ]) if self.pk else 0

        return stock_investment + crypto_investment

    def save(self, *args, **kwargs):
        # 객체를 데이터베이스에 저장
        super().save(*args, **kwargs)
        
        # 저장 이후에 총 투자 금액 계산
        if self.pk:
            self.total_investment = self.calculate_total_investment()
            # 업데이트된 total_investment를 다시 저장
            super().save(update_fields=["total_investment"])

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

    def calculate_profit(self):
        if self.current_value:
            return (self.current_value - self.purchase_price) * float(self.quantity)
        return None

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

    def calculate_profit(self):
        if self.current_value:
            return (self.current_value - self.purchase_price) * float(self.quantity)
        return None

    def __str__(self):
        return f"{self.name} ({self.symbol}) in {self.portfolio.name}"


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

