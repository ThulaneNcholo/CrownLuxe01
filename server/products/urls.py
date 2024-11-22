
from django.urls import path
from .import views

urlpatterns = [
    path('products',views.AllProductsView,name='products'),
    path('view-product/<int:id>',views.ProductView,name='view-product'),
]

