from django.db import models

from django.contrib.gis.db import models as gis_models


class ReserveAirspace(gis_models.Model):
    """
    This is the main model class to create reserve airspace
    it inherits from the following models
    from django.contrib.gis.db import models as gis_models
    the geom extends the models' PolygonField. Thus we can only draw polygons
    A multipolygonField would have given us ability to draw lines as well
    """

    geom = gis_models.PolygonField(blank=True, null=True)

    """
    # objects = gis_models.GeoManager()
    objects = GeoManager()

    The objects field is a modelclass manager that inherits from Geodjango's default manager
    NB: This is slightly diffrent for Django 2+ users
    """

    name = models.CharField(max_length=255, blank=True, null=True)

    centroid = gis_models.PointField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if self.geom:
            self.centroid = self.geom.centroid

        super(ReserveAirspace, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
