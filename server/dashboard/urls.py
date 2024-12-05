
from django.urls import path
from .import views

urlpatterns = [
    path('dashboard',views.DashboardView,name='dashboard'),
    path('order-view/<int:id>',views.OrderViewAdmin,name='order-view'),
    path('admin-products',views.AdminItemsView,name='admin-products'),
    path('product-view-admin/<int:id>',views.ViewProductAdminView,name='product-view-admin'),

    path('product/new/',views.NewProductView,name='new-product'),
    path('product/<int:product_id>/edit/',views.NewProductView, name='product_edit'),


    path('product-details-partial',views.ProductDetailsPartialView,name='create-details'),
    path('remove-session-item',views.RemoveItemSessionView,name='remove-session-item'),
    path('remove-object-admin/<int:id>',views.RemoveMainProductDetailsView,name='remove-object-admin'),
]

