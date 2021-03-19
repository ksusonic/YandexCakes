from django.db import models


class Region(models.Model):
    region = models.IntegerField()


class WorkingHours(models.Model):
    working_hours = models.CharField(max_length=11)

    # TODO parse time from model


class Courier(models.Model):
    courier_id = models.AutoField(primary_key=True)

    FOOT = 'foot'
    BIKE = 'bike'
    CAR = 'car'
    COURIER_TYPES = [  # Тип <-> грузоподъемность
        (FOOT, '10'),
        (BIKE, '15'),
        (CAR, '50')
    ]
    courier_type = models.CharField(
        max_length=4,
        choices=COURIER_TYPES,
    )

    regions = models.ManyToManyField(Region)
    working_hours = models.ManyToManyField(WorkingHours)
