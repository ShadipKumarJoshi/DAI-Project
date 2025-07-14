from django.urls import path
from . import views
from core.views.sme_profile_form_wizard import SMERegistrationWizard


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('notice/', views.notice, name='notice'),
    path('notice/<int:pk>/', views.notice_detail, name='notice-detail'),
    path('news/', views.news, name='news'),
    path('news/<int:pk>/', views.news_detail, name='news-detail'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('cms/', views.cms_list_view, name='cms-list'),
    path('<slug:slug>/', views.cms_page_view, name='cms_page'),

    path('register', views.register, name='register'),
    path('register/type/', views.register_type, name='register_type'),
    path('register/sme/', views.sme_register, name='sme_register'),
    path('register/bdsp/', views.bdsp_register, name='bdsp_register'),
    path('sme/profile/form', SMERegistrationWizard.as_view(),
         name='sme_profile_wizard'),
    path('sme/profile/', views.sme_profile_view, name='sme_profile_view'),
    path('bdsp/profile/', views.bdsp_profile_view, name='bdsp_profile_view'),
    path('bdsp/profile/form/', views.bdsp_profile_form, name='bdsp_profile_form'),





    path('dashboard', views.dashboard, name='dashboard'),
    # Dynamic dashboard routing
    path('dashboard/<str:model_name>/',
         views.dashboard_model_list, name='dashboard_model_list'),
    path('dashboard/<str:model_name>/add/',
         views.dashboard_model_add, name='dashboard_model_add'),
    path('dashboard/<str:model_name>/<int:pk>/edit/',
         views.dashboard_model_edit, name='dashboard_model_edit'),
    path('dashboard/<str:model_name>/<int:pk>/delete/',
         views.dashboard_model_delete, name='dashboard_model_delete'),




    path('dummy', views.dummy, name='dummy'),
]
