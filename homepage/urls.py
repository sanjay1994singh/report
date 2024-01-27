from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('get-services/', views.get_services, name='get_services'),
    path('article/', views.create_article, name='create_article'),
    path('download_report/', views.download_report, name='download_report'),


    path('my_service/', views.my_service, name='my_service'),
    path('get-my-services/', views.get_my_services, name='get_my_services'),

    path('buy_service_detail/<int:service_id>/', views.buy_service_detail, name='buy_service_detail'),
    path('get_service_month/', views.get_service_month, name='get_service_month'),
    path('get_service_price/', views.get_service_price, name='get_service_price'),
    path('payment_success/', views.payment_success, name='payment_success'),
]
