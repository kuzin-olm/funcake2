import os
from datetime import datetime

import aiofiles
from loguru import logger
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import File, FileType


async def save_prev_img_recipe(db: Session, recipe_uuid: int, file: UploadFile):
    path = settings.STATIC_DIR / "recipe" / str(recipe_uuid) / "prev"
    path = await save_file(path, file)
    db.add(File(path=str(path), type=FileType.image_preview, uuid_recipe=recipe_uuid))


async def save_other_img_recipe(db: Session, recipe_uuid: int, file: UploadFile):
    path = settings.STATIC_DIR / "recipe" / str(recipe_uuid) / "other"
    path = await save_file(path, file)
    db.add(File(path=str(path), type=FileType.image_other, uuid_recipe=recipe_uuid))


async def save_doc_recipe(db: Session, recipe_uuid: int, file: UploadFile):
    path = settings.STATIC_DIR / "recipe" / str(recipe_uuid) / "doc"
    path = await save_file(path, file)
    db.add(File(path=str(path), type=FileType.document, uuid_recipe=recipe_uuid))


async def save_file(to: str, file: UploadFile, chunk: int = None) -> str:
    if not os.path.exists(to):
        os.makedirs(to)

    timestamp = datetime.utcnow().timestamp()
    timestamp = "_".join(str(timestamp).split("."))
    to /= f"{timestamp}_{file.filename}"

    try:
        async with aiofiles.open(to, 'wb') as out_file:
            if chunk:
                while content := await file.read(chunk):
                    await out_file.write(content)
            else:
                content = await file.read()
                await out_file.write(content)
    except Exception as err:
        logger.error(f"ERROR:    File {file.filename} save error, {err}.")
    finally:
        file.file.close()

    return to
