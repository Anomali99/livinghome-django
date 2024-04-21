from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.home),
    path('admin/', views.admin),
    path('logout/', views.logout),
    path('product/', views.product),
    path('detail/<id>', views.detail),
    path('web/<token>', api.webLink),
    path('ig/<token>', api.igLink),
    path('fb/<token>', api.fbLink),
]