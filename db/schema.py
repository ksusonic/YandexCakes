from enum import Enum as PyEnum, unique

from sqlalchemy import Column, Integer, Enum, ARRAY, String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    # Именование индексов
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    # Именование уникальных индексов
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    # Именование CHECK-constraint-ов
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    # Именование внешних ключей
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    # Именование первичных ключей
    'pk': 'pk__%(table_name)s'
}

Base = declarative_base(metadata=MetaData(naming_convention=convention))


@unique
class CourierType(PyEnum):
    foot = 'foot'
    bike = 'bike'
    car = 'car'


class Courier(Base):
    __tablename__ = 'courier'
    courier_id = Column(Integer, primary_key=True)
    courier_type = Column(Enum(CourierType, name='courier_type'), nullable=False)
    regions = Column(ARRAY(Integer), nullable=False)
    working_hours = Column(ARRAY(String), nullable=False)

    def to_dict(self) -> dict:
        return {
            'courier_id': self.courier_id,
            'courier_type': self.courier_type.name,
            'regions': self.regions,
            'working_hours': self.working_hours
        }

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
