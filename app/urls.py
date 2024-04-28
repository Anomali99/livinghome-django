from django.urls import path
from . import views
from . import api
from . import testing

urlpatterns = [
    path('', views.home),
    path('admin/', views.admin),
    path('logout/', views.logout),
    path('product/', views.product),
    path('detail/<id>', views.detail),
    path('monitoring/', views.monitoring),
    path('web/<token>', api.webLink),
    path('ig/<token>', api.igLink),
    path('fb/<token>', api.fbLink),
    path('dummy/<token>', testing.dummy),
    path('remove/', testing.remove),
    path('remove/comment', testing.removeComment),
]