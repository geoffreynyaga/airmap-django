from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin

from .models import ReserveAirspace


class ReserveAirspaceAdmin(LeafletGeoAdmin):
    list_display = ("name",)


admin.site.register(ReserveAirspace, ReserveAirspaceAdmin)
