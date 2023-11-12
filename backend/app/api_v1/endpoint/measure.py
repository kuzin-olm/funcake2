from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.api_v1.crud.measure import get_all_measures
from app.api_v1.dependencies import verify_auth
from app.api_v1.schema.measure import Measure
from app.db.connector import get_db

router = APIRouter(
    prefix="/measure",
    tags=["measure"],
    dependencies=[Depends(verify_auth)],
)


@router.get("", status_code=status.HTTP_200_OK, response_model=List[Measure])
async def get_measures(db: Session = Depends(get_db)):
    measures = get_all_measures(db=db)
    return measures
