from app.api_v1.schema.base import CamelModel


class Measure(CamelModel):
    uuid: int
    name: str

    class Config:
        orm_mode = True
