from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Geo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    polygon = models.PolygonField()
    name = models.CharField(max_length=50)
    price = models.IntegerField()

    def __str__(self):
        return self.name + " Polygon"
