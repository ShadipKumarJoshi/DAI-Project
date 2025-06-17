from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dummy', views.dummy, name='dummy'),
    path('notice/', views.notice, name='notice'),
    path('notice/<int:pk>/', views.notice_detail, name='notice-detail'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),

    
    
]
