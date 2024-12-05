
from django.urls import path
from .import views

urlpatterns = [
    path('login',views.LoginPageView,name='login'),
    path('logout/', views.LogoutUser,name="logout"),
]

