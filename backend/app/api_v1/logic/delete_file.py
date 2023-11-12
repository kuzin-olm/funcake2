import os

from sqlalchemy import and_, not_
from sqlalchemy.orm import Session

from app import models
from app.models import FileType


def delete_prev_img_recipe(db: Session, recipe_uuid: int) -> None:
    delete_except_current_files_from_recipe(db, recipe_uuid, [], FileType.image_preview)


def delete_except_current_files_from_recipe(
        db: Session,
        recipe_uuid: int,
        current_files_uuid: list,
        file_type: FileType
) -> None:
    """
    Удаление файлов рецепта путем исключения.

    Parameters:
        db: текущя сессия с бд
        recipe_uuid: uuid рецепта, у которого удаляем файлы
        current_files_uuid: список uuid`ов файлов, которые надо оставить, а все остальные будут удалены
        file_type: фильтрация по типу фалов
    """
    files = db.query(models.File).filter(
        and_(
            not_(models.File.uuid.in_(current_files_uuid)),
            models.File.uuid_recipe == recipe_uuid,
            models.File.type == file_type
        )
    )
    files_path = [file.path for file in files]
    try:
        files.delete()
        delete_files(files_path)
        db.commit()
    except FileNotFoundError:
        db.commit()
    except:
        db.rollback()


def delete_files(files: list[str]) -> None:
    for file in files:
        os.remove(file)

