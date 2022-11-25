import uuid

from tortoise import fields

from apps.core.common import models as base_models
from apps.flow import models as flow_models
from apps.applicant import models as applicant_models


class Application(base_models.UUIDDBModel, base_models.TimeStampModel):
    identifier = fields.UUIDField(index=True)
    flow_name = fields.CharField(max_length=128)

    applicant_id: uuid.UUID
    applicant: fields.ForeignKeyNullableRelation["applicant_models.Applicant"] = fields.ForeignKeyField(
        "models.Applicant", null=True, related_name="applications"
    )

    flow: fields.OneToOneRelation["flow_models.Flow"]
    steps: fields.ForeignKeyRelation["flow_models.Step"]
