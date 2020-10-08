from django.urls import path

from . import views

urlpatterns = [
    path('', views.ParkingView.as_view(), name='parking'),
    path('health', views.health, name='health')
]
