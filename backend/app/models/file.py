import enum
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.db.database import Base


class FileType(enum.Enum):
    image_preview = "img_prev"
    image_other = "img_other"
    document = "doc"


class File(Base):
    __tablename__ = "file"

    uuid = Column(Integer, primary_key=True, index=True)
    path = Column(String, default=None)
    type = Column(Enum(FileType), default=None)
    uuid_recipe = Column(Integer, ForeignKey("recipe.uuid", ondelete="CASCADE"))

    recipe = relationship("Recipe", back_populates="files", uselist=False)
