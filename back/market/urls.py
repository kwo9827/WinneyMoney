from django.urls import path
from .import views

urlpatterns = [
    path('search/', views.search),
    path('search/coin/', views.search_coin)
]
