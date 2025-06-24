from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
     # Dynamic dashboard routing
    path('dashboard/<str:model_name>/', views.dashboard_model_list, name='dashboard_model_list'),
    path('dashboard/<str:model_name>/add/', views.dashboard_model_add, name='dashboard_model_add'),
    path('dashboard/<str:model_name>/<int:pk>/edit/', views.dashboard_model_edit, name='dashboard_model_edit'),
    path('dashboard/<str:model_name>/<int:pk>/delete/', views.dashboard_model_delete, name='dashboard_model_delete'),
    
]
