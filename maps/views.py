from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic import CreateView

from .models import ReserveAirspace
from .forms import ReserveAirspaceForm


class HomePageView(TemplateView):

    template_name = "maps/map.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['latest_articles'] = Article.objects.all()[:5]
    #     return context


def all_airspace_datasets(request):

    # serialize("geojson", City.objects.all(), geometry_field="point", fields=("name",))
    my_reserve_airspace = ReserveAirspace.objects.all()
    path = serialize(
        "geojson",
        my_reserve_airspace,
        geometry_field="geom",
        fields=("name", "centroid"),
    )

    # print(path, "path")
    return HttpResponse(path, content_type="json")


def my_reserve_datasets(request):
    airspace = serialize(
        "geojson", ReserveAirspace.objects.filter(created_by=request.user)
    )
    return HttpResponse(airspace, content_type="json")


class ReserveAirspaceCreateView(CreateView):
    """ TO DO: Restrict Pending Flights to 10 to reduce spamming
        --FIXED by queryset count and if-else in templates
    """

    form_class = ReserveAirspaceForm
    model = ReserveAirspace
    template_name = "maps/create1.html"
    success_url = "/maps/map"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ReserveAirspaceCreateView, self).get_context_data(
    #         *args, **kwargs
    #     )

    #     my_pending_airspaces = ReserveAirspace.objects.filter(
    #         created_by=self.request.user
    #     ).filter(status=0)

    #     context["my_pending_approval_airspaces"] = my_pending_airspaces.order_by("-id")[
    #         :10
    #     ]
    #     context["my_pending_approval_airspaces_count"] = my_pending_airspaces.count()
    #     # context['myflightlogs'] = FlightLog.objects.filter(user=thisuser)
    #     return context


class OldReserveAirspaceCreateView(CreateView):
    """ TO DO: Restrict Pending Flights to 10 to reduce spamming
        --FIXED by queryset count and if-else in templates
    """

    form_class = ReserveAirspaceForm
    model = ReserveAirspace
    template_name = "maps/create2.html"
    success_url = "/maps/map"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ReserveAirspaceCreateView, self).get_context_data(
    #         *args, **kwargs
    #     )

    #     my_pending_airspaces = ReserveAirspace.objects.filter(
    #         created_by=self.request.user
    #     ).filter(status=0)

    #     context["my_pending_approval_airspaces"] = my_pending_airspaces.order_by("-id")[
    #         :10
    #     ]
    #     context["my_pending_approval_airspaces_count"] = my_pending_airspaces.count()
    #     # context['myflightlogs'] = FlightLog.objects.filter(user=thisuser)
    #     return context
