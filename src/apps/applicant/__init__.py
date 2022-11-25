from enum import Enum


class ApplicantStatus(str, Enum):
    ACTIVATED = 'ACTIVATED'
    DEACTIVATED = 'DEACTIVATED'
    BANNED = 'BANNED'


class ApplicantType(str, Enum):
    ...
