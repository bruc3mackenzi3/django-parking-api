from django.urls import path

from . import views
from .views import ParkingQueryView, ParkingRatesView

urlpatterns = [
    path('query', ParkingQueryView.as_view(), name='parking_query'),
    path('rates', ParkingRatesView.as_view(), name='parking_rates'),
    path('ready', views.ready, name='ready'),
    path('health', views.health, name='health')
]
