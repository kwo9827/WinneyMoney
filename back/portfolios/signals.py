from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Portfolio, Stock, Crypto, PortfolioDeposit, PortfolioSaving

# Portfolio의 total_investment 및 allocation 업데이트 함수
def update_portfolio_totals(portfolio):
    """
    Portfolio의 총 자산과 변동성, 비율을 업데이트.
    """
    # Portfolio의 계산 메서드를 호출
    portfolio.total_investment = portfolio.calculate_total_investment()
    portfolio.allocation = portfolio.calculate_allocation()
    portfolio.total_volatility = portfolio.calculate_total_volatility()  # 변동성 계산

    # 필요한 필드만 업데이트
    portfolio.save(update_fields=['total_investment', 'allocation', 'total_volatility'])

# Stock 추가/수정/삭제 시 Portfolio 업데이트
@receiver(post_save, sender=Stock)
@receiver(post_delete, sender=Stock)
def update_portfolio_on_stock_change(sender, instance, **kwargs):
    update_portfolio_totals(instance.portfolio)

# Crypto 추가/수정/삭제 시 Portfolio 업데이트
@receiver(post_save, sender=Crypto)
@receiver(post_delete, sender=Crypto)
def update_portfolio_on_crypto_change(sender, instance, **kwargs):
    update_portfolio_totals(instance.portfolio)

# PortfolioDeposit 추가/수정/삭제 시 Portfolio 업데이트
@receiver(post_save, sender=PortfolioDeposit)
@receiver(post_delete, sender=PortfolioDeposit)
def update_portfolio_on_deposit_change(sender, instance, **kwargs):
    update_portfolio_totals(instance.portfolio)

# PortfolioSaving 추가/수정/삭제 시 Portfolio 업데이트
@receiver(post_save, sender=PortfolioSaving)
@receiver(post_delete, sender=PortfolioSaving)
def update_portfolio_on_saving_change(sender, instance, **kwargs):
    update_portfolio_totals(instance.portfolio)