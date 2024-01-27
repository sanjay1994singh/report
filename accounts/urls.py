from django.urls import path
from . import views
urlpatterns = [
    path('login-user/', views.login_user, name='login_user'),
    path('signup-user/', views.signup_user, name='signup_user'),
    path('logout-user/', views.logout_user, name='logout_user'),

    path('term-condition/', views.term_condition, name='term-condition'),
    path('shipping-delivery/', views.shipping_delivery, name='shipping-delivery'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('cancellation-refund/', views.cancellation_refund, name='cancellation-refund'),

]
