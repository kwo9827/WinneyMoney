from django.urls import path
from . import views

urlpatterns = [
    # 포트폴리오 목록 조회 및 생성
    path('', views.portfolio_list_create, name='portfolio-list-create'),

    # 개별 포트폴리오 조회, 수정, 삭제
    path('<int:portfolio_id>/', views.portfolio_detail, name='portfolio-detail'),

    # 포트폴리오에 주식 추가
    path('<int:portfolio_id>/stocks/', views.add_stock, name='add-stock'),

    # 주식 수정 및 삭제
    path('<int:portfolio_id>/stocks/<int:stock_id>/', views.update_stock, name='update-stock'),
    path('<int:portfolio_id>/stocks/<int:stock_id>/delete/', views.delete_stock, name='delete-stock'),

    # 포트폴리오에 암호화폐 추가
    path('<int:portfolio_id>/crypto/', views.add_crypto, name='add-crypto'),

    # 암호화폐 수정 및 삭제
    path('<int:portfolio_id>/crypto/<int:crypto_id>/', views.update_crypto, name='update-crypto'),
    path('<int:portfolio_id>/crypto/<int:crypto_id>/delete/', views.delete_crypto, name='delete-crypto'),

    # 포트폴리오에 추천 예/적금 조회
    path('<int:portfolio_id>/recommend/', views.recommend_products, name='recommend-products'),
]
