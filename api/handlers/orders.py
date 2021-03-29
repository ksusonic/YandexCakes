from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from db.base import Session

from api.schema import Order, Orders
from db.schema import Order as OrderSchema

router = APIRouter(prefix="/orders")


@router.post('/')
async def post_orders(order_list: Orders):
    db = Session()
    order_ids = []
    order_fail_ids = []
    for order in order_list.data:
        db_order = OrderSchema(
            order_id=order.order_id,
            weight=order.weight,
            region=order.region,
            delivery_hours=order.delivery_hours
        )
        db.add(db_order)
        try:
            db.commit()
        except IntegrityError:
            order_fail_ids.append(order.order_id)
        else:
            db.refresh(db_order)
            order_ids.append(order.order_id)

    if len(order_fail_ids) == 0:
        return JSONResponse(content={'couriers': [{'id': c_id} for c_id in order_ids]},
                            status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={"validation_error": {
            'couriers': [{'id': c_id} for c_id in order_fail_ids]}}, status_code=status.HTTP_400_BAD_REQUEST)
