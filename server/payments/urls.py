
from django.urls import path
from .import views

urlpatterns = [
    path('Payments-view/<str:id>',views.PaymentsView,name='Payments-view'),
    path('Cancel-Payment',views.CancelPaymentView,name='Cancel-Payment'),
    path('notify',views.NotifyView,name='notify'),
]

