from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from datetime import datetime, timedelta
import requests

@api_view(['GET'])
def exchange(request, fromCountry, price):
    # 환율 정보 가져오기
    API_KEY = settings.CURRENCY_API_KEY
    # st_data = str(int(st_date) - 1)
    # URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={API_KEY}&searchdate={st_data}&data=AP01'
    URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={API_KEY}&data=AP01'
    requestData = requests.get(URL)
    todayresult = requestData.json()

    exchange_rate= 1
    exchangeresult= 1

    # 환율 계산
    for data in todayresult:
        if data.get('cur_unit') == fromCountry:
            exchange_rate = float(data.get('deal_bas_r').replace(',',''))
            exchangeresult = price * exchange_rate
            break
    
    # if howlong == '-1':
    #     date_diff = 3
    # else:
    #     stringdate = howlong.replace('-', '')
    #     date1 = datetime.strptime(st_date, '%Y%m%d')
    #     date2 = datetime.strptime(stringdate, '%Y%m%d')
    #     date_diff = date1 - date2
    #     date_diff = date_diff.days
    
    
    # exchangeresult = round(exchangeresult , 3)
    # date1 = datetime.strptime(st_date, "%Y%m%d")
    # yesterday = date1 - timedelta(days=date_diff)
    # yesterday = yesterday.strftime("%Y%m%d")  

    # yesterday=str(yesterday)
    # print(yesterday)
    # NEWURL = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={API_KEY}&searchdate={yesterday}&data=AP01"
    # response = requests.get(NEWURL)
    # print("HTTP Status Code:", response.status_code)  # 상태 코드 확인 
    # yesterdayresult = response.json()
    # print(response)
    # print(yesterdayresult)
    # # result = {}

    # id = 1
    # for today_currency in todayresult:
    #     today_country = today_currency["cur_nm"]
    #     today_deal_bas_r = float(today_currency["deal_bas_r"].replace(",", ""))
    #     if today_country == "한국 원":
    #             continue
    #     for yesterday_currency in yesterdayresult:
    #         if today_country == yesterday_currency["cur_nm"]:
    #             yesterday_deal_bas_r = float(yesterday_currency["deal_bas_r"].replace(",", ""))
    #             diff_percent = round((today_deal_bas_r - yesterday_deal_bas_r) / yesterday_deal_bas_r * 100, 3)
    #             result[str(id)] = [today_country, today_deal_bas_r, diff_percent]
    #             id += 1
    #             break
    #     else:
    #         result[str(id)] = [today_country, today_deal_bas_r, None]
    #         id += 1

    # return Response({"exchangeresult": exchangeresult, 'diff' : result})
    return Response({"exchangeresult": exchangeresult})

def news(request):
    query = '경제'
    display_count = 100
    page = int(request.GET.get('page', 1))
    
    url = 'https://openapi.naver.com/v1/search/news.json'
    headers = {
        'X-Naver-Client-Id': settings.NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': settings.NAVER_CLIENT_SECRET,
    }
    params = {
        'query': query,
        'display': display_count,
        'start': (page - 1) * 10 + 1,  # 페이지 시작 번호
        'sort': 'date',
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return JsonResponse({'error': '네이버 API 호출 실패'}, status=response.status_code)

    news_data = response.json().get('items', [])
    
    # 페이지네이션
    paginator = Paginator(news_data, 10)  # 한 페이지당 10개
    current_page_data = paginator.get_page(page)

    return JsonResponse({
        'news': list(current_page_data),
        'total_pages': paginator.num_pages,
        'current_page': current_page_data.number,
    }, safe=False)

