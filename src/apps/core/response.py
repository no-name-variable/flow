import typing
from apps.core.common.schemas import BaseResponseModel


def handle_response(content: typing.Any):
    return BaseResponseModel(data=content)

