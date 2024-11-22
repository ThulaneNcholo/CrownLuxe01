
from django.urls import path
from .import views

urlpatterns = [
    path('',views.IndexView,name='index'),
    path('load-content',views.IndexView,name='load-content'),
    path('contact-us',views.ContactUsView,name='contact-us'),
    path('about-us',views.AboutView,name='about-us'),
    path('our-reviews',views.ReviewsView,name='our-reviews'),
    path('catalog-list/<int:id>',views.CatalogListView,name='catalog-list'),
    
]

