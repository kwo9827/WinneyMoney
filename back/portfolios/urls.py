from django.urls import path
from .import views

urlpatterns = [
    path('', views.portfolio_list_create, name='portfolio-list-create'),  # 포트폴리오 목록 조회 및 생성
    path('<int:portfolio_id>/', views.portfolio_detail, name='portfolio-detail'),  # 개별 포트폴리오 조회, 수정, 삭제
    path('<int:portfolio_id>/stocks/', views.add_or_update_stock, name='add_stock'),  # 포트폴리오에 주식 추가
    path('<int:portfolio_id>/bonds/', views.add_bond, name='add_bond'),  # 포트폴리오에 채권 추가
    path('<int:portfolio_id>/recommend/', views.recommend_savings, name='recommend_savings'),  # 포트폴리오에 추천 예/적금 조회
]
