from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dummy', views.dummy, name='dummy'),
    path('notice/', views.notice, name='notice'),
    path('notice/<int:pk>/', views.notice_detail, name='notice-detail'),
    path('news/', views.news, name='news'),
    path('news/<int:pk>/', views.news_detail, name='news-detail'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('<slug:slug>/', views.cms_page_view, name='cms_page'),

    
    
]
