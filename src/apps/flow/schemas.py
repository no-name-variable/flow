from turtle import title
from uuid import UUID

from pydantic import BaseModel, Field

from apps.flow import StepStatusEnum


class Step(BaseModel):
    step: str
    description: str | None = Field(title="Полное описание шага")
    is_first_step: bool = False
    retry_period: int = Field(title="Период времени в секнуднах когда можно перевызывать шаг", default=60 * 30)
    next_step: str | None = Field(title="Название следующего шага")
    on_status: StepStatusEnum = Field(title="Статус шага для перехода на следующий шаг", default=StepStatusEnum.FINISH)
    next_step_if_error: str | None = Field(title="Следующий шаг при вознекновении ошибки")


class FlowRequestModel(BaseModel):
    identifier: UUID
    steps: list[Step]


class FlowMapResponseModel(BaseModel):
    flow: str
    step: str
    is_first_step: bool = False
    retry_period: int = Field(title="Период времени в секнуднах когда можно перевызывать шаг", default=60 * 30)
    next_step: str | None = Field(title="Название следующего шага")
    next_step_if_error: str | None = Field(title="Следующий шаг при вознекновении ошибки")