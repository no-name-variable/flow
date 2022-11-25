import uuid

from fastapi import APIRouter, Response, Depends

from apps.core.common.schemas import BaseResponseModel
from apps.core.response import handle_response
from apps.flow import controllers as flow_controllers
from apps.flow import schemas as flow_schemas

router = APIRouter(prefix="/flows")


@router.post("/create-flow")
async def create_flow(
        flow_request: flow_controllers.CreateFlowService = Depends()
):
    await flow_request.create_steps_by_current_flow()

    return Response(status_code=201)


@router.get(
    "/flow-map",
    response_model=BaseResponseModel[
        list[flow_schemas.FlowMapResponseModel]
    ]
)
async def flow_map(
    controller: "flow_controllers.FlowController" = Depends()
):
    flow_maps = await controller.flow_map()
    return handle_response(flow_maps)


@router.get("/current-step")
async def current_step_path(
    controller: "flow_controllers.FlowController" = Depends()
):
    current_step = await controller.current_step
    return handle_response(current_step)


@router.get("/next-step")
async def next_step_path(
    controller: "flow_controllers.FlowController" = Depends()
):
    next_step = await controller.next_step
    return handle_response(next_step)


@router.put("/next-step-if-error")
async def next_step_if_error_path(
    controller: "flow_controllers.FlowController" = Depends(),
    reason: str = ""
):
    await controller.terminate_step_with_error(reason)
    return Response(status_code=201)


@router.get("/set-next-step")
async def set_next_step_path(
    controller: "flow_controllers.FlowController" = Depends()
):
    await controller.terminate_step_successfully()
    return Response(status_code=201)