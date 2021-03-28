from .couriers import router as post_couriers
from .courier import router as get_courier

ROUTERS = (
    post_couriers, get_courier,  # TODO all routers
)
