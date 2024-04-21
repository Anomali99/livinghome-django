from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('admin/', views.admin),
    path('logout/', views.logout),
    path('product/', views.product),
]