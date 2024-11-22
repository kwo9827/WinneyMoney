from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:article_pk>/', views.article_detail, name='article_detail'),
    path('comment/<int:article_pk>/<int:parent_pk>/', views.comments_create, name='comments_create'),
    path('comment/<int:article_pk>/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('comment/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
    path('<int:article_pk>/like/', views.toggle_like_article, name='toggle_like_article'),

]