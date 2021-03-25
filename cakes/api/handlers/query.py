from sqlalchemy import and_, func, select

from cakes.db.schema import couriers_table

COURIERS_QUERY = select([
    couriers_table.c.courier_id,
    couriers_table.c.courier_type,
    couriers_table.c.regions,
    couriers_table.c.working_hours
])
