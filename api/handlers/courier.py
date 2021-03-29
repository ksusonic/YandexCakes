from fastapi import APIRouter, status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from api.schema import PatchCourier
from db.base import Session
from db.schema import Courier as CourierSchema

router = APIRouter(prefix="/couriers")


@router.get('/{courier_id}')
async def get_courier(courier_id: int):
    db = Session()
    query = db.query(CourierSchema).get(courier_id)
    # TODO дополнительные поля и подсчет рейтинга!
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Courier not found")
    return JSONResponse(query.to_dict())


@router.patch('/{courier_id}')
async def patch_courier(courier_id: int, data: PatchCourier):
    db = Session()
    query = db.query(CourierSchema).get(courier_id)
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Courier not found")
    else:

        if data.courier_type and data.regions and data.working_hours:
            query.regions = data.regions
            db.commit()
            return JSONResponse(query.to_dict(), status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong fields")
