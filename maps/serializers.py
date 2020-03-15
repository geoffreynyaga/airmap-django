from .models import ReserveAirspace
from rest_framework import serializers


class MapAPISerializer(serializers.ModelSerializer):
    # date_timesince = serializers.ReadOnlyField(source="format_timesince")
    # last_c2b = serializers.ReadOnlyField(source="get_last_c2b")

    class Meta:
        model = ReserveAirspace
        fields = (
            "name",
            "geom",
        )
