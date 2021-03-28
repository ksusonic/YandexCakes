from enum import Enum as PyEnum, unique

from sqlalchemy import Column, Integer, Enum, JSON

from db.base import Base


@unique
class CourierType(PyEnum):
    foot = 'foot'
    bike = 'bike'
    car = 'car'


class Courier(Base):
    __tablename__ = 'courier'
    courier_id = Column(Integer, primary_key=True)
    courier_type = Column(Enum(CourierType, name='courier_type'), nullable=False)
    regions = Column(JSON, nullable=False)
    working_hours = Column(JSON, nullable=False)

    @classmethod
    def weight(cls):
        weight_values = {
            'foot': 10,
            'bike': 15,
            'car': 50
        }
        if cls.courier_type == CourierType.foot:
            return weight_values['foot']
        elif cls.courier_type == CourierType.bike:
            return weight_values['bike']
        elif cls.courier_type == CourierType.car:
            return weight_values['car']
        else:
            raise ValueError("No such courier type")
