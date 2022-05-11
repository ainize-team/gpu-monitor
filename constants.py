from enum import Enum


class ExitStatusEnum(Enum):
    """
    Values for the `__status` in `sys.exit()`.
    """

    PARAMETER_VALUE_ERROR = 1
    NVIDIA_SMI_NOT_FOUND_ERROR = 2


class SlackMesaageColorEnum(Enum):
    """
    Slack message color value according to status
    """

    SUCCESS_MESSAGE_COLOR = "#28a745"
    ERROR_MESSAGE_COLOR = "#dc3545"
