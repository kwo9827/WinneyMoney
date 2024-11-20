from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('detail/<str:username>/', views.user_detail, name='user_detail'),
    path('delete/', views.delete_user, name='delete_user'),
    path('edit/', views.edit_user, name='edit_user'),
    path('change-password/', views.change_password, name='change_password'),
    path('follow/<str:username>/', views.follow, name='follow'),
]
