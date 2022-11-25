import uuid
from typing import TYPE_CHECKING

from tortoise import fields

from apps.core.common import models as base_models
from apps.flow import StepStatusEnum, FlowTypeEnum

if TYPE_CHECKING:
    from apps.applications import models as application_models
    from apps.applicant import models as applicant_models


class Event(base_models.BaseDBModel, base_models.TimeStampModel):
    event = fields.CharField(max_length=1024, null=True)

    step_id: int
    step: fields.ForeignKeyNullableRelation['Step'] = fields.ForeignKeyField("models.Step", null=True)


class Step(base_models.BaseDBModel, base_models.TimeStampModel):
    """
    retry period: cast to seconds
    """

    is_first_step = fields.BooleanField(default=False)
    step = fields.CharField(max_length=128)
    status = fields.CharEnumField(StepStatusEnum, max_length=128, null=True)
    reason = fields.CharField(max_length=1024, null=True)
    retry_period = fields.IntField(default=60*30)
    description = fields.CharField(max_length=1024, null=True)

    next_step_id: int
    next_step: fields.ForeignKeyNullableRelation["Step"] = fields.ForeignKeyField(
        "models.Step",
        related_name="steps",
        null=True
    )
    next_step_if_error: fields.ForeignKeyNullableRelation["Step"] = fields.ForeignKeyField(
        "models.Step",
        related_name="error_steps",
        null=True
    )
    application_id: uuid.UUID
    application: fields.ForeignKeyNullableRelation["application_models.Application"] = fields.ForeignKeyField(
        "models.Application",
        null=True
    )

    flow: fields.ForeignKeyNullableRelation["Flow"] = fields.ForeignKeyField("models.Flow", null=True)
    events: fields.ReverseRelation["Event"]


class Flow(base_models.BaseDBModel):
    flow_type = fields.CharEnumField(enum_type=FlowTypeEnum, max_length=128)
    flow_name = fields.CharField(max_length=128)

    is_active = fields.BooleanField(default=True)

    application_id: uuid.UUID
    application: fields.ForeignKeyNullableRelation["application_models.Application"] = fields.OneToOneField(
        "models.Application", null=True, related_name="flow"
    )
    applicant_id: uuid.UUID
    applicant: fields.ForeignKeyNullableRelation['applicant_models.Applicant'] = fields.ForeignKeyField(
        "models.Applicant", null=True, related_name="flows"
    )

    steps: fields.ReverseRelation["Step"]
