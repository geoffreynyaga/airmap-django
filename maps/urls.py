from django.contrib import admin
from django.urls import path, include


from .views import (
    HomePageView,
    all_airspace_datasets,
    ReserveAirspaceCreateView,
    OldReserveAirspaceCreateView,
    ReserveCreateAPIView,
)

urlpatterns = [
    path("map/", HomePageView.as_view(), name="home"),
    path("airspace-geojson/", all_airspace_datasets, name="airspace-geojson"),
    path("create/", ReserveAirspaceCreateView.as_view(), name="create_reserve"),
    path("old-create/", OldReserveAirspaceCreateView.as_view(), name="create_reserve"),
    path("api/create/", ReserveCreateAPIView.as_view(), name="create_reserve_api"),
]
