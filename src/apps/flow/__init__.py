from enum import Enum


class StepStatusEnum(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    FINISH = "FINISH"
    FAILED = "FAILED"


class FlowTypeEnum(str, Enum):
    MAIN = "MAIN"
    PUBLIC = "PUBLIC"
