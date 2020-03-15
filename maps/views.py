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
    template_name = "maps/create3.html"
    # success_url = "/maps/map"

    def post(self, request, *args, **kwargs):

        print(self.request, "request")
        print((self.request.POST), "request.POST")

        x = ReserveAirspace.objects.create(
            name=self.request.POST["name"], geom=self.request.POST["geom"]
        )

        print(x, "x")

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


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class ReserveCreateAPIView(APIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        import json

        print(request.data, "in API")
        name = request.data["name"]
        # geom = json.loads(request.data["geom"])
        geom = json.loads(request.data["geom"])

        print(name, "name")
        print(geom, "geom")

        # print(json.loads(geom), " type geom")
        # print(dir(geom), " dir geom")

        """

        {
        "type":"FeatureCollection",
        "features":[
        {"type":"Feature","properties":{},
        "geometry":{"type":"Polygon",
                    "coordinates":[
                        [
                            [36.901230812072754,-1.3365200875255174],
                            [36.901230812072754,-1.3341603846017482],
                            [36.903719902038574,-1.3341603846017482],
                            [36.903719902038574,-1.3365200875255174],
                            [36.901230812072754,-1.3365200875255174]
                        ]
                    ]
                }}
            ]}
        """

        geom_type = geom["features"][0]["geometry"]["type"]

        coords = geom["features"][0]["geometry"]["coordinates"][0]
        print(coords, "coords")

        from django.contrib.gis.geos import (
            GEOSGeometry,
            LineString,
            MultiLineString,
            Polygon,
        )

        if geom_type == "Polygon":
            multi_line = Polygon(coords)
            print(multi_line, "multi_line")

        # line = LineString(coords)
        # print(line, "line")

        x = ReserveAirspace.objects.create(name=name, geom=multi_line)
        print(x, "x instance")

        return Response(
            {"ResultDesc": "Reserve Airspace Created successfully"},
            content_type="application/json",
            status=status.HTTP_201_CREATED,
        )
