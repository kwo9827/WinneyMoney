from . import views
from django.urls import path

app_name = 'finlife'

urlpatterns = [
    # 정기예금 상품 목록 DB에 저장
    path('save-deposit-products/', views.save_deposit_products, name='save_deposit_products'),

    # 전체 정기예금 상품 목록 출력 & 데이터 삽입
    path('deposit-products/', views.deposit_products, name='deposit_products'),

    # 특정 상품의 옵션 리스트 출력
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options, name='deposit_product_options'),

    # 특정 금융 상품을 즐겨찾기에 추가하거나 제거하는 기능
    path('favorite/<str:fin_prdt_cd>/', views.favorite, name='favorite'),

    #사용자의 즐겨찾기 목록을 조회
    path('user-favorites/', views.user_favorites, name='user_favorites'),
]
