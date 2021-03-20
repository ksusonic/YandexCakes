from django.db import models


class Region(models.Model):
    region = models.IntegerField()


class WorkingHours(models.Model):
    working_hours = models.CharField(max_length=11)

    # TODO parse time from model


class Courier(models.Model):
    courier_id = models.AutoField(primary_key=True)

    class CourierTypes(models.IntegerChoices):
        FOOT = 10
        BIKE = 15
        CAR = 50

    courier_type = models.IntegerField(choices=CourierTypes.choices)
    regions = models.ManyToManyField(Region, )
    working_hours = models.ManyToManyField(WorkingHours)
