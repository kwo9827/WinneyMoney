from . import views
from django.urls import path

app_name = 'finlife'

urlpatterns = [
    # 정기예금/적금 상품 목록 DB에 저장
    path('save-deposit-products/', views.save_deposit_products, name='save_deposit_products'),
    path('save-saving-products/', views.save_saving_products),

    # 전체 정기예금 상품 목록 출력 & 데이터 삽입
    path('deposit-products/', views.deposit_products, name='deposit_products'),
    path('deposit-products/detail/<int:product_id>/', views.deposit_detail),

    # 전체 적금 상품 목록 출력 & 데이터 삽입
    path('saving-products/', views.saving_products),
    path('saving-products/detail/<int:product_id>/', views.saving_detail),

    # 예금 즐겨찾기 추가/제거
    path('favorites/deposit/<str:fin_prdt_cd>/', views.favorite_deposit, name='favorite_deposit'),

    # 적금 즐겨찾기 추가/제거
    path('favorites/saving/<str:fin_prdt_cd>/', views.favorite_saving, name='favorite_saving'),

    # 즐겨찾기 조회
    path('favorites/', views.user_favorites, name='user_favorites'),
]
