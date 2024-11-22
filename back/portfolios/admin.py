from django.contrib import admin
from .models import Portfolio, Stock, Bond

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'total_investment', 'created_at')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'portfolio', 'ticker', 'purchase_price', 'quantity', 'current_value', 'created_at')

@admin.register(Bond)
class BondAdmin(admin.ModelAdmin):
    list_display = ('id', 'portfolio', 'name', 'investment', 'current_value', 'yield_rate', 'maturity_date', 'created_at')
