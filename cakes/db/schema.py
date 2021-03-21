from enum import Enum, unique
import sqlalchemy.types as types
from sqlalchemy import Table, Column, Integer, String, ARRAY, Time, MetaData, ForeignKey, Enum as PgEnum

# https://docs.sqlalchemy.org/en/13/core/constraints.html#configuring-constraint-naming-conventions
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)


@unique
class CourierType(Enum):
    foot = 'foot'
    bike = 'bike'
    car = 'car'


# TODO class CourierWorkTime(types.TypeDecorator):


couriers_table = Table(
    'couriers',
    metadata,
    Column('courier_id', Integer, primary_key=True),
    Column('courier_type', PgEnum(CourierType, name='courier_type'), nullable=False),
    Column('regions', ARRAY(Integer), nullable=False),
    Column('working_hours', ARRAY(String), nullable=False)
)
