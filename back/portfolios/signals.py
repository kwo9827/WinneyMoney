from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Portfolio, Stock, Crypto

# Portfolio의 total_investment 및 volatility 업데이트 함수
def update_portfolio_totals(portfolio):
    # 총 투자 금액 계산
    total_investment = sum(stock.total_investment for stock in portfolio.stocks.all()) + \
                       sum(crypto.total_investment for crypto in portfolio.cryptocurrencies.all())
    portfolio.total_investment = total_investment

    # 변동성 계산 (예시: 평균 변동성을 계산)
    stock_volatility = [stock.volatility for stock in portfolio.stocks.all() if stock.volatility is not None]
    crypto_volatility = [crypto.volatility for crypto in portfolio.cryptocurrencies.all() if crypto.volatility is not None]
    all_volatility = stock_volatility + crypto_volatility

    portfolio.volatility = sum(all_volatility) / len(all_volatility) if all_volatility else None
    portfolio.save(update_fields=['total_investment', 'volatility'])

# Stock 추가 및 수정 시 Portfolio 업데이트
@receiver(post_save, sender=Stock)
def update_portfolio_on_stock_save(sender, instance, **kwargs):
    update_portfolio_totals(instance.portfolio)

# Stock 삭제 시 Portfolio 업데이트
@receiver(post_delete, sender=Stock)
def update_portfolio_on_stock_delete(sender, instance, **kwargs):
    update_portfolio_totals(instance.portfolio)

# Crypto 추가 및 수정 시 Portfolio 업데이트
@receiver(post_save, sender=Crypto)
def update_portfolio_on_crypto_save(sender, instance, **kwargs):
    update_portfolio_totals(instance.portfolio)

# Crypto 삭제 시 Portfolio 업데이트
@receiver(post_delete, sender=Crypto)
def update_portfolio_on_crypto_delete(sender, instance, **kwargs):
    update_portfolio_totals(instance.portfolio)
