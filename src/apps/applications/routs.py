import uuid

from fastapi import APIRouter, Response

from apps.applications import models as application_models

router = APIRouter(prefix="/flows")


@router.post("/create-application/{identifier}")
async def create_application(
        identifier: uuid.UUID,
        flow_name: str
):
    await application_models.Application.create(identifier=identifier, flow_name=flow_name)

    return Response(status_code=201)