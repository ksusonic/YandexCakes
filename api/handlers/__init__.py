from .couriers import router as couriers
from .courier import router as courier

ROUTERS = (
    couriers, courier,   # TODO all routers
)
