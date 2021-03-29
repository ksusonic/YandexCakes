from .couriers import router as couriers
from .courier import router as courier
from .orders import router as orders

ROUTERS = (
    couriers, courier, orders
)
