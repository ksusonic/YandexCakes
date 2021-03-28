import time
from typing import List, Optional
from pydantic.main import BaseModel


def check_work_time(list_times: list) -> bool:
    for t in list_times:
        if not time.strptime(t.split('-')[0], '%H:%M').tm_hour < time.strptime(t.split('-')[1], '%H:%M').tm_hour:
            return False
    return True


class PatchCourier(BaseModel):
    courier_type: Optional[str]
    regions: Optional[List[Optional[int]]]
    working_hours: Optional[List[Optional[str]]]


class Courier(PatchCourier):
    courier_id: int
    courier_type: str
    regions: List[Optional[int]]
    working_hours: List[Optional[str]]


class Couriers(BaseModel):
    data: List[Courier]
