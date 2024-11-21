from django.urls import path
from .import views

urlpatterns = [
    path('<str:fromCountry>/<int:price>/', views.exchange),
    # path('<str:fromCountry>/<int:price>/<str:st_date>/<str:howlong>/', views.exchange),
]