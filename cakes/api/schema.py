"""
Модуль содержит схемы для валидации данных в запросах и ответах.
"""
from marshmallow import Schema  # , ValidationError, validates, validates_schema
from marshmallow.fields import Dict, Int, List, Nested, Str, Time
from marshmallow.validate import Length, OneOf, Range

from cakes.db.schema import CourierType

TIME_INTERVAL_FORMAT = '%H:%M-%H:%M'


class PatchCourierSchema(Schema):
    courier_type = Str(validate=OneOf([cour_type.value for cour_type in CourierType]))
    regions = List(Int(validate=Range(min=0)), strict=True)
    working_hours = Str(format=TIME_INTERVAL_FORMAT, validate=Length(equal=11), strict=True)


class CourierSchema(Schema):
    courier_id = Int(validate=Range(min=0), strict=True, required=True)
    courier_type = Str(validate=OneOf([cour_type.value for cour_type in CourierType]), required=True)
    regions = List(Int(validate=Range(min=0), strict=True), required=True)
    working_hours = Str(format=TIME_INTERVAL_FORMAT, validate=Length(equal=11), required=True)


class CourierImportSchema(PatchCourierSchema):
    couriers = Nested(CourierSchema, many=True, required=True,
                      validate=Length(max=10000))


class WorkingHours(Schema):
    working_hours_id = Int(validate=Range(min=0), strict=True, required=True)
    start_time = Time(required=True)
    finish_time = Time(required=True)


class Region(Schema):
    region = Int(validate=Range(min=0), strict=True, required=True)
