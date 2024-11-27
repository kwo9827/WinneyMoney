from django.db import models

class SearchIndex(models.Model):
    name = models.CharField(max_length=255)  # 회사 이름
    ticker = models.CharField(max_length=20)  # 종목 코드
    market = models.CharField(max_length=50)  # 시장 이름 (예: KOSPI, NASDAQ)
    currency = models.CharField(max_length=10, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)  # 데이터 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 데이터 갱신 시간

    def __str__(self):
        return f"{self.name} ({self.ticker}) - {self.market}"

class SearchCoin(models.Model):
    symbol = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)  # 데이터 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 데이터 갱신 시간

    def __str__(self):
        return f"{self.symbol}"