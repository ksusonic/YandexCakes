from django.db import models


# class Region(models.Model):
#     region = models.IntegerField()
#
#
# class WorkingHours(models.Model):
#     working_hours = models.CharField(max_length=11)
#
#     # TODO parse time from model


class Courier(models.Model):
    courier_id = models.AutoField(primary_key=True)

    FOOT = 10
    BIKE = 15
    CAR = 50
    COURIER_TYPES = [  # Тип <-> грузоподъемность
        (FOOT, 'foot'),
        (BIKE, 'bike'),
        (CAR, 'car')
    ]
    courier_type = models.IntegerField(
        choices=COURIER_TYPES,
    )

    regions = models.IntegerField()  # models.ManyToManyField(Region)
    working_hours = models.CharField(max_length=11)  # models.ManyToManyField(WorkingHours)

    def __str__(self):
        return self.courier_id
