import requests
from django.core.management.base import BaseCommand
from market.models import SearchCoin


class Command(BaseCommand):
    help = "Load cryptocurrency data into the SearchCoin model from Coinone API"

    def handle(self, *args, **kwargs):
        # Coinone API URL
        url = "https://api.coinone.co.kr/public/v2/markets/KRW"
        
        try:
            self.stdout.write(self.style.WARNING("Loading cryptocurrency data from Coinone..."))

            # API 호출
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"API 요청 실패: {response.status_code} - {response.text}")

            data = response.json().get("markets", [])
            if not data:
                raise Exception("API 응답에 데이터가 없습니다.")

            # 데이터 저장/갱신
            for market in data:
                symbol = market.get("target_currency")
                
                if not symbol:
                    continue  # 데이터가 없으면 스킵

                # 데이터 저장 또는 업데이트
                SearchCoin.objects.update_or_create(
                    symbol=symbol,
                )
            
            self.stdout.write(self.style.SUCCESS("Successfully loaded cryptocurrency data."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to load cryptocurrency data: {e}"))
