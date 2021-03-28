from typing import List, Optional
from pydantic.main import BaseModel


class PatchCourier(BaseModel):
    courier_type: Optional[str]
    regions: Optional[List[Optional[int]]]
    working_hours: Optional[List[Optional[str]]]


class Courier(BaseModel):
    courier_id: int
    courier_type: str
    regions: List[Optional[int]]
    working_hours: List[Optional[str]]


class Couriers(BaseModel):
    data: List[Courier]
