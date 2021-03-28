from fastapi import APIRouter, status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

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
