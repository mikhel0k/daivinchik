from enum import Enum


class SexAllowed(str, Enum):
    male = "male"
    female = "female"


class StatusAllowed(str, Enum):
    active = "active"
    inactive = "inactive"