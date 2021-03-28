from pydantic.class_validators import Optional, List
from pydantic.main import BaseModel
from sqlalchemy import Column, Integer, String, ARRAY, Float
from sqlalchemy.orm import relationship


class Courier(BaseModel):
    courier_id: int
    courier_type: str
    regions: List[Optional[int]]
    working_hours: List[Optional[str]]


