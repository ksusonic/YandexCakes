from fastapi import APIRouter, status
from sqlalchemy import and_
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from db.base import Session

from api.schema import Order, Orders, Courier, CourierID, CourierType
from db.schema import Order as OrderSchema, Courier as CourierSchema

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


@router.post('/assign')
async def assign_post(courier_id: CourierID):
    response_ids = []
    default_response = JSONResponse({'orders': response_ids})
    db = Session()
    courier_from_db = db.query(CourierSchema).get(courier_id.courier_id)
    if not courier_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Courier not found")

    query = db.query(OrderSchema).filter(
        and_(OrderSchema.region.in_(courier_from_db.regions)),
        (OrderSchema.weight <= CourierType(courier_from_db.courier_type).weight()),
    ).all()

