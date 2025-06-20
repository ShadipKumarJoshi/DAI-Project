from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('notice/', views.notice, name='notice'),
    path('notice/<int:pk>/', views.notice_detail, name='notice-detail'),
    path('news/', views.news, name='news'),
    path('news/<int:pk>/', views.news_detail, name='news-detail'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('<slug:slug>/', views.cms_page_view, name='cms_page'),
    
    

    path('dashboard', views.dashboard, name='dashboard'),
    
    
    
    
    path('dummy', views.dummy, name='dummy'),
]
