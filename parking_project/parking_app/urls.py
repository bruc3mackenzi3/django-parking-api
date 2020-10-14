from django.urls import path

from .views import ParkingQueryView, ParkingRatesView, health

urlpatterns = [
    path('query', ParkingQueryView.as_view(), name='parking_query'),
    path('rates', ParkingRatesView.as_view(), name='parking_rates'),
    path('health', health, name='health')
]
