from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('download_report/', views.download_report, name='download_report'),
]
