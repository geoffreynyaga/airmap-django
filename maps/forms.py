from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets


from leaflet.forms.widgets import LeafletWidget


from .models import ReserveAirspace


class ExtLeafletWidget(LeafletWidget):
    geometry_field_class = "geom"


class ReserveAirspaceForm(forms.ModelForm):
    class Meta:
        model = ReserveAirspace

        fields = ("name", "geom")
        widgets = {
            "geom": ExtLeafletWidget(),
        }
