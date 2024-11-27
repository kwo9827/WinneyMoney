import FinanceDataReader as fdr
from django.core.management.base import BaseCommand
from market.models import SearchIndex

class Command(BaseCommand):
    help = "Load market data into the SearchIndex model"

    def handle(self, *args, **kwargs):
        # 국내 주식 (currency='KRW')와 해외 주식 (currency='USD') 구분
        markets = {
            'KOSPI': ('KRW', fdr.StockListing('KOSPI')),
            'KONEX': ('KRW', fdr.StockListing('KONEX')),
            'NASDAQ': ('USD', fdr.StockListing('NASDAQ')),
            'S&P500': ('USD', fdr.StockListing('S&P500')),
            'NYSE': ('USD', fdr.StockListing('NYSE')),
            'AMEX': ('USD', fdr.StockListing('AMEX')),
        }

        for market, (currency, data) in markets.items():
            try:
                self.stdout.write(self.style.WARNING(f"Loading data for {market}..."))
                
                # 데이터 저장
                for _, row in data.iterrows():
                    # 종목 코드 컬럼 구분
                    ticker_col = 'Symbol' if 'Symbol' in data.columns else 'Code'
                    
                    # 데이터 저장/갱신
                    SearchIndex.objects.update_or_create(
                        ticker=row[ticker_col],
                        market=market,
                        defaults={
                            'name': row['Name'],
                            'currency': currency,
                        }
                    )
                
                self.stdout.write(self.style.SUCCESS(f"Successfully loaded data for {market}."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to load data for {market}: {e}"))
