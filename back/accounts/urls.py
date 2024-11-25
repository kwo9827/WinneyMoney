from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('detail/<str:username>/', views.user_detail, name='user_detail'), # 회원정보 상세보기
    path('delete/', views.delete_user, name='delete_user'), # 회원탈퇴
    path('edit/', views.edit_user, name='edit_user'), # 회원수정
    path('change-password/', views.change_password, name='change_password'), # 비밀번호 변경
    path('follow/<str:username>/', views.follow, name='follow'), # 팔로우
    # path('password-reset/', views.password_reset_request, name='password_reset_request'), # 비밀번호 재설정 요청
    # path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'), # 비밀번호 재설정 확인
]

