from django.urls import path
from .import views

urlpatterns = [
    path('cart-items/<str:id>',views.CartView,name='cart-items'),
    path('contact-details/<str:id>',views.CustomerContactView,name='contact-details'),
    path('payment-successful',views.PaymentSuccessfulView,name='payment-successful'),

]

