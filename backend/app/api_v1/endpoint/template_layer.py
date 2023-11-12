from typing import List

from fastapi import APIRouter, status, Depends, Body, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.adapter import RepoManager
from app.db.connector import get_db, get_service, get_repo
from app.api_v1.dependencies import verify_auth
from app.api_v1.crud.template_layer import TemplateLayerService
from app.api_v1.schema.template_layer import TemplateLayer, TemplateLayerCreate, TemplateLayerUpdate


router = APIRouter(
    prefix="/template-layer",
    tags=["template layer"],
    dependencies=[Depends(verify_auth)],
)


# todo?
# service_template_layer = get_service(TemplateLayerService)
# @router.get("", status_code=status.HTTP_200_OK, response_model=List[TemplateLayer])
# async def get_templates(service: TemplateLayerService = Depends(service_template_layer)):
#     return service.get_all()


# @router.get("", status_code=status.HTTP_200_OK, response_model=List[TemplateLayer])
# async def get_templates(repo: RepoManager = Depends(get_repo)):
#     return repo.template.get_all()


@router.get("", status_code=status.HTTP_200_OK, response_model=List[TemplateLayer])
async def get_templates(db: Session = Depends(get_db)):
    return TemplateLayerService(db).get_all()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TemplateLayer)
async def create_template(template: TemplateLayerCreate = Body(), db: Session = Depends(get_db)):
    try:
        return TemplateLayerService(db).create(template)
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Не верные данные.")


@router.put("/{uuid}", status_code=status.HTTP_200_OK, response_model=TemplateLayer)
async def update_template(uuid: int, template: TemplateLayerUpdate = Body(), db: Session = Depends(get_db)):
    try:
        return TemplateLayerService(db).update(uuid, template)
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Не верные данные.")


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(uuid: int, db: Session = Depends(get_db)):
    try:
        TemplateLayerService(db).delete(uuid)
        return
    except HTTPException as err:
        raise err
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Не верные данные.")
    except:
        raise HTTPException(status_code=400, detail="Не получилось удалить.")
