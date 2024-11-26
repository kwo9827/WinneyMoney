from django.urls import path
from .import views

app_name = 'info'

urlpatterns = [
    path('news/', views.news, name='news'), # 뉴스
    path('<str:fromCountry>/<int:price>/', views.exchange), # 환전
    path('foreign/<str:fromCountry>/<int:price>/', views.exchange_foreign), # 환전
    # path('<str:fromCountry>/<int:price>/<str:st_date>/<str:howlong>/', views.exchange),
    path('chat/', views.chat_with_gpt, name='chat_with_gpt'),  # 챗봇
]