from typing import Optional
from enum import Enum


class ServiceStatus(str, Enum):
    SUCCESS = "SUCCESS"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    SUBJECT_NOT_FOUND = "SUBJECT_NOT_FOUND"
    NOT_FOUND = "NOT_FOUND"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class BaseServiceError(Exception):
    code: str
    description: str = None

    def __init__(self, description: Optional[str] = None):
        if self.description is None or description:
            self.description = description

        super().__init__(self.description)


class SubjectNotFoundError(BaseServiceError):
    code = ServiceStatus.SUBJECT_NOT_FOUND.value
    description = "Не найдено"


class ServiceUnavailableError(BaseServiceError):
    code = ServiceStatus.SERVICE_UNAVAILABLE.value
    description = "Сервис не доступен"


class ServiceUnknownError(BaseServiceError):
    code = ServiceStatus.UNKNOWN_ERROR.value