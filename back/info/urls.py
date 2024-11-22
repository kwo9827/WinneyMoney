from django.urls import path
from .import views

app_name = 'info'

urlpatterns = [
    path('news/', views.news, name='news'),
    path('<str:fromCountry>/<int:price>/', views.exchange),
    # path('<str:fromCountry>/<int:price>/<str:st_date>/<str:howlong>/', views.exchange),
]