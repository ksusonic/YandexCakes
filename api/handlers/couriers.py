from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from db.base import Session

from api.schema import Couriers, check_work_time
from db.schema import Courier as CourierSchema

router = APIRouter(prefix="/couriers")


@router.post('/')
async def post_couriers(courier_list: Couriers):
    db = Session()
    courier_ids = []
    courier_fail_ids = []
    for courier in courier_list.data:
        db_courier = CourierSchema(
            courier_id=courier.courier_id,
            courier_type=courier.courier_type,
            regions=courier.regions,
            working_hours=courier.working_hours
        )
        if not check_work_time(courier.working_hours):
            courier_fail_ids.append(courier.courier_id)
            continue

        db.add(db_courier)
        try:
            db.commit()
        except IntegrityError:
            courier_fail_ids.append(courier.courier_id)
        else:
            db.refresh(db_courier)
            courier_ids.append(courier.courier_id)

    if len(courier_fail_ids) == 0:
        return JSONResponse(content={'couriers': [{'id': c_id} for c_id in courier_ids]},
                            status_code=status.HTTP_201_CREATED)
    else:
        return JSONResponse(content={"validation_error": {
            'couriers': [{'id': c_id} for c_id in courier_fail_ids]}}, status_code=status.HTTP_400_BAD_REQUEST)
