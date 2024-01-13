from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('get-services/', views.get_services, name='get_services'),
    path('article/', views.create_article, name='create_article'),
    path('download_report/', views.download_report, name='download_report'),
]
