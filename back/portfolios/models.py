from django.db import models
from django.conf import settings
from finlife.models import DepositProducts, SavingProducts
from datetime import date

User = settings.AUTH_USER_MODEL

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolios")
    name = models.CharField(max_length=100)
    total_investment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
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

    recommended_deposits = models.ManyToManyField(
        DepositProducts,
        related_name="recommended_portfolios",
        blank=True
    )
    selected_deposits = models.ManyToManyField(
        DepositProducts,
        related_name="selected_portfolios",
        blank=True
    )
    recommended_savings = models.ManyToManyField(
        SavingProducts,
        related_name="recommended_portfolios",
        blank=True
    )
    selected_savings = models.ManyToManyField(
        SavingProducts,
        related_name="selected_portfolios",
        blank=True
    )

    def calculate_total_investment(self):
        stock_investment = sum([stock.purchase_price * stock.quantity for stock in self.stocks.all()])
        bond_investment = sum([bond.investment for bond in self.bonds.all()])
        return stock_investment + bond_investment

    def save(self, *args, **kwargs):
        self.total_investment = self.calculate_total_investment()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Portfolio: {self.name}"


class Stock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="stocks")
    ticker = models.CharField(max_length=10)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.PositiveIntegerField()
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_profit(self):
        return (self.current_value - self.purchase_price) * self.quantity

    def __str__(self):
        return f"{self.ticker} in {self.portfolio.name}"


class Bond(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="bonds")
    name = models.CharField(max_length=100)
    investment = models.DecimalField(max_digits=15, decimal_places=2)
    current_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    yield_rate = models.FloatField()
    maturity_date = models.DateField(default=date(2024, 12, 31))
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_yield_rate(self):
        return ((self.current_value - self.investment) / self.investment) * 100

    def __str__(self):
        return f"{self.name} in {self.portfolio.name}"


class UserResponse(models.Model):
    portfolio = models.OneToOneField(Portfolio, on_delete=models.CASCADE, related_name="user_response")
    current_step = models.PositiveIntegerField(default=0)  # 사용자가 어디까지 응답했는지 저장
    responses = models.JSONField(default=dict)  # 각 단계별 응답 데이터를 저장

    def __str__(self):
        return f"Responses for {self.portfolio.name}"


class RecommendationLog(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="recommendation_logs")
    product = models.ForeignKey(
        DepositProducts,
        on_delete=models.CASCADE,
        related_name="recommendation_logs",
        blank=True,
        null=True
    )
    reason = models.TextField(blank=True, null=True)  # 추천 이유
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.portfolio.name}"
