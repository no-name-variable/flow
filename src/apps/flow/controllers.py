import uuid

from fastapi import Query

from apps.core.exceptions import SubjectNotFoundError
from apps.flow import models as flow_models
from apps.applications import models as application_models
from apps.flow import schemas as flow_schemas

from apps.flow import StepStatusEnum


class CreateFlowService:
    def __init__(self, flow_request: flow_schemas.FlowRequestModel = None):
        self.flow_request = flow_request

    async def get_current_application(self) -> "application_models.Application":
        application = await application_models.Application.filter(identifier=self.flow_request.identifier).first()
        if not application:
            raise SubjectNotFoundError()

        return application

    async def create_flow(self) -> tuple["flow_models.Flow", bool]:
        """
        Первый метод в контролере, для запуска процесса создания флоу
        :return:
        tuple["flow_models.Flow", bool]
        """
        application = await self.get_current_application()
        flow_name: str = application.flow_name

        flow, is_created = await flow_models.Flow.get_or_create(
            flow_type=flow_name.upper(), application=application
        )
        return flow, is_created

    async def create_next_step(self):
        for request_step in self.flow_request.steps:
            if request_step.next_step:
                step = await flow_models.Step.filter(step__icontains=request_step.step.upper()).first()
                next_step = await flow_models.Step.filter(step__icontains=request_step.next_step.upper()).first()
                step.next_step_id = next_step.id
                await step.save(update_fields=['next_step_id'])

    async def create_steps_by_current_flow(self):
        flow, is_created = await self.create_flow()

        for request_step in self.flow_request.steps:
            await flow_models.Step.get_or_create(
                is_first_step=request_step.is_first_step,
                step=request_step.step.upper(),
                flow=flow,
                retry_period=request_step.retry_period,
            )

        await self.create_next_step()


class FlowController:

    def __init__(self, identifier: uuid.UUID = Query()):
        self.identifier = identifier

    async def application(self) -> "application_models.Application":
        application = await application_models.Application.filter(identifier=self.identifier).first()
        if not application:
            raise SubjectNotFoundError

        return application

    async def terminate_step_successfully(self):
        step = await self.current_step
        step.status = StepStatusEnum.FINISH
        await step.save(update_fields=['status'])
        await self.set_next_step_application()

    async def terminate_step_with_error(self, reason: str):
        step = await self.current_step
        step.reason = reason
        step.status = StepStatusEnum.FAILED
        await step.save(update_fields=['reason', 'status'])
        await self.set_next_step_application()

    async def set_next_step_application(self):
        application = await self.application()
        current_step = await self.current_step
        next_step = await self.next_step
        next_step_if_error = await self.next_step_error
        if current_step.status == StepStatusEnum.FAILED and next_step_if_error:
            next_step_if_error.application_id = application.subject_identifier
            await next_step_if_error.save(update_fields=['application_id'])

        if next_step and current_step.status != StepStatusEnum.FAILED:
            next_step.application_id = application.subject_identifier
            await next_step.save(update_fields=['application_id'])

    async def flow_map(self) -> list[dict]:
        application = await self.application()
        flow = await application.flow
        steps = await flow.steps.all().order_by('created_at')
        steps_list = []
        for step in steps:
            step: "flow_models.Step" = await step
            next_step = await step.next_step
            next_step_if_error = await step.next_step_if_error
            flow = await application.flow

            data = {
              "flow": flow.flow_type,
              "step": step.step,
              "is_first_step": step.is_first_step,
              "retry_period": step.retry_period,
              "next_step": next_step.step if next_step else "",
              "next_step_if_error": next_step_if_error.step if next_step_if_error else ""
            }
            steps_list.append(data)

        return steps_list

    @property
    async def current_step(self) -> "flow_models.Step":
        application = await self.application()
        step = await application.steps.order_by("-created_at").first()
        if not step:
            flow = await application.flow
            first_step: "flow_models.Step" = await flow.steps.filter(is_first_step=True).first()
            first_step.application_id = application.subject_identifier
            await first_step.save(update_fields=['application_id'])
            return first_step

        return step

    @property
    async def next_step(self) -> "flow_models.Step":
        step: "flow_models.Step" = await self.current_step
        return await step.next_step

    @property
    async def next_step_error(self) -> flow_models.Step | str:
        step: "flow_models.Step" = await self.current_step
        next_step_if_error = await step.next_step_if_error
        if next_step_if_error:
            return next_step_if_error
        return ""










