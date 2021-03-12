from enum import Enum, unique

from sqlalchemy import (
    MetaData,
    Column, Date, Enum as PgEnum, ForeignKey,
    ForeignKeyConstraint, Integer, String, Table
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
metadata = MetaData(naming_convention=convention)


@unique
class CourierType(Enum):
    foot = 'foot'
    bike = 'bike'
    car = 'car'


imports_table = Table(
    'imports',
    metadata,
    Column('import_id', Integer, primary_key=True)
)

couriers_table = Table(
    'couriers',
    metadata,
    Column('import_id', Integer, ForeignKey('imports.import_id'), primary_key=True)
    Column('courier_id', Integer, primary_key=True),
    Column('courier_type', PgEnum(CourierType, name='courier_type'), nullable=False),
    # Column('regions', )
)
