import time
from typing import List, Optional

from fastapi.exceptions import RequestValidationError
from pydantic import validator
from pydantic.main import BaseModel

from db.schema import CourierType


class PatchCourier(BaseModel):
    courier_type: Optional[CourierType]
    regions: Optional[List[Optional[int]]]
    working_hours: Optional[List[Optional[str]]]

    @validator('working_hours')
    def working_hours_check(cls, working_hours):
        for t in working_hours:
            if not (time.strptime(t.split('-')[0], '%H:%M') < time.strptime(t.split('-')[1], '%H:%M')):
                raise RequestValidationError("Incorrect working_hours")
        return working_hours


class Courier(PatchCourier):
    courier_id: int
    courier_type: CourierType
    regions: List[Optional[int]]
    working_hours: List[Optional[str]]

    @validator('working_hours')
    def working_hours_check(cls, working_hours):
        for t in working_hours:
            if not time.strptime(t.split('-')[0], '%H:%M') < time.strptime(t.split('-')[1], '%H:%M'):
                raise RequestValidationError("Incorrect working_hours")
        return working_hours


class Couriers(BaseModel):
    data: List[Courier]


class Order(BaseModel):
    order_id: int
    weight: float
    region: int
    delivery_hours: List[str]

    @validator('weight')
    def weight_check(cls, weight):
        if not 0.01 <= weight <= 50:
            raise RequestValidationError("Incorrect weight")
        return weight

    @validator('delivery_hours')
    def working_hours_check(cls, delivery_hours):
        for t in delivery_hours:
            if not time.strptime(t.split('-')[0], '%H:%M') < time.strptime(t.split('-')[1], '%H:%M'):
                raise RequestValidationError("Incorrect delivery_hours")
        return delivery_hours


class Orders(BaseModel):
    data: List[Order]


class CourierID(BaseModel):
    courier_id: int


def check_courier_time_for_order(courier: Courier, order: Order) -> bool:
    pass


