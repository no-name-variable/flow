from typing import Generic, TypeVar

from pydantic import BaseModel, validator
from pydantic.generics import GenericModel

from apps.core.exceptions import ServiceStatus

DataT = TypeVar('DataT')


class BaseOrmModeModel(BaseModel):

    class Config:
        orm_mode = True


class Error(BaseModel):
    message: str


class BaseResponseModel(GenericModel, Generic[DataT]):
    code: ServiceStatus = ServiceStatus.SUCCESS
    data: DataT | None
    error: Error | None

    @validator('error', always=True)
    def check_consistency(cls, v, values):
        if v is not None and values['data'] is not None:
            raise ValueError('must not provide both data and error')
        if v is None and values.get('data') is None:
            raise ValueError('must provide data or error')
        return v