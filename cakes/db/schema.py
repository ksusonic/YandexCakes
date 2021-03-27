from enum import Enum, unique

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    MetaData, Column, Enum as PgEnum, ForeignKey, Integer,
    String, Table, Time
)

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
metadata = Base.metadata


class WorkingHours(Base):
    __tablename__ = 'working_hours'
    working_hours_id = Column(Integer, primary_key=True)
    start_time = Column(Time, nullable=False)
    finish_time = Column(Time, nullable=False)


courier_working_hours_table = Table(
    'courier_working_hours', metadata,
    Column('courier_id', Integer, ForeignKey('courier.courier_id')),
    Column('working_hours_id', Integer, ForeignKey('working_hours.working_hours_id'))
)


class Region(Base):
    __tablename__ = 'region'
    region = Column(Integer, primary_key=True)


courier_region_table = Table(
    'courier_region', metadata,
    Column('courier_id', Integer, ForeignKey('courier.courier_id')),
    Column('region', Integer, ForeignKey('region.region'))
)


@unique
class CourierType(Enum):
    foot = 'foot'
    bike = 'bike'
    car = 'car'


class Courier(Base):
    __tablename__ = 'courier'
    courier_id = Column(Integer, primary_key=True)
    courier_type = Column(PgEnum(CourierType, name='courier_type'), nullable=False)
    regions = relationship("Region", secondary=courier_region_table)
    working_hours = relationship("WorkingHours", secondary=courier_working_hours_table)
