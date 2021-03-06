from enum import Enum as PyEnum, unique

from sqlalchemy import Column, Integer, Enum, ARRAY, String, Float, DateTime, ForeignKey

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

    def weight(self):
        weight_values = {
            'foot': 10,
            'bike': 15,
            'car': 50
        }

        if self.foot:
            return weight_values['foot']
        elif self.bike:
            return weight_values['bike']
        else:
            return weight_values['car']


class Courier(Base):
    __tablename__ = 'courier'
    courier_id = Column(Integer, primary_key=True)
    courier_type = Column(Enum(CourierType, name='courier_type'), nullable=False)
    regions = Column(ARRAY(Integer), nullable=False)
    working_hours = Column(ARRAY(String), nullable=False)

    def weight(self):
        weight_values = {
            'foot': 10,
            'bike': 15,
            'car': 50
        }

        if self.courier_type.foot:
            return weight_values['foot']
        elif self.courier_type.bike:
            return weight_values['bike']
        else:
            return weight_values['car']

    def to_dict(self) -> dict:
        return {
            'courier_id': self.courier_id,
            'courier_type': self.courier_type.name,
            'regions': self.regions,
            'working_hours': self.working_hours
        }


class Order(Base):
    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    region = Column(Integer, nullable=False)
    delivery_hours = Column(ARRAY(String), nullable=False)
    courier_id_assigned = Column(Integer, nullable=True)

    def to_dict(self) -> dict:
        return {
            'order_id': self.order_id,
            'weight': self.weight,
            'regions': self.regions,
            'delivery_hours': self.delivery_hours
        }
