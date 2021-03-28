from sqlalchemy import select

from cakes.db.schema import Courier

COURIERS_QUERY = select([
    Courier.courier_id,
    Courier.courier_type,
    Courier.regions,
    Courier.working_hours
])
