from app.api_v1.mixin.schema_mixin import ORJSONParserMixin
from app.api_v1.schema.base import CamelModel
from pydantic import validator, Field


class UserAuthenticate(ORJSONParserMixin, CamelModel):
    nickname: str
    password: str


class UserCreate(ORJSONParserMixin, CamelModel):
    nickname: str = Field(..., min_length=4, max_length=30)
    password1: str
    password2: str

    @validator('nickname')
    def name_must_not_space(cls, v):
        if ' ' in v:
            raise ValueError('В имени не должно быть пробелов.')
        return v

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('Пароли не совпадают.')
        return v


class UserInDb(CamelModel):
    uuid: int
    nickname: str
    is_admin: bool

    class Config:
        orm_mode = True


class UserAuthorize(UserInDb):
    hashed_password: str
