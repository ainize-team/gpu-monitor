from enum import Enum


class ExitStatusEnum(Enum):
    """
    Possible values for the `__status` in `sys.exit()`.
    """

    PARAMETER_VALUE_ERROR = 1
    NVIDIA_SMI_NOT_FOUND_ERROR = 2
