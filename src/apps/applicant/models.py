from tortoise import fields

from apps.applications import models as application_models
from apps.flow import models as flow_models
from apps.core.common import models as base_models


class Applicant(base_models.UUIDDBModel, base_models.TimeStampModel):
    name = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=True)

    flows: fields.ReverseRelation['flow_models.Flow']
    applications: fields.ReverseRelation['application_models.Application']


