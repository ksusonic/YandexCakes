from datetime import datetime

from fastapi import APIRouter, status
from sqlalchemy import and_
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from db.base import Session

from api.schema import Order, Orders, Courier, CourierID, check_courier_time_for_order, OrderDone
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
    default_response = JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    db = Session()
    courier_from_db = db.query(CourierSchema).get(courier_id.courier_id)
    if not courier_from_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Courier not found")

    query = db.query(OrderSchema).filter(
        and_(OrderSchema.region.in_(courier_from_db.regions)),
        (OrderSchema.weight <= courier_from_db.courier_type.weight())
    ).all()

    if not query:
        return default_response

    for order in query:
        if check_courier_time_for_order(courier_from_db.working_hours, order.delivery_hours):
            order.courier_id_assigned = courier_from_db.courier_id
            response_ids.append(order.order_id)
    if response_ids:
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            'orders': [{'id': id_} for id_ in response_ids],
            'assign_time': datetime.now().isoformat()[:-4] + 'Z'
        })
    else:
        return default_response


@router.post('/complete')
async def complete_post(order: OrderDone):
    db = Session()
    courier_from_db = db.query(CourierSchema).get(order.courier_id)
    order_from_db = db.query(OrderSchema).get(order.order_id)

    if not courier_from_db or not order_from_db or courier_from_db.courier_id != order.courier_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong courier or order id")

    # TODO count rating

    db.delete(order_from_db)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'order_id': order.order_id
    })
