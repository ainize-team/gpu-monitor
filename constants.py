from enum import Enum


class ExitStatusEnum(Enum):
    """
    Values for the `__status` in `sys.exit()`.
    """

    PARAMETER_VALUE_ERROR = 1
    NVIDIA_SMI_NOT_FOUND_ERROR = 2


class SlackMessageTypeEnum(Enum):
    """
    Values for the slack message status.
    """

    SUCCESS_MESSAGE = "success"
    ERROR_MESSAGE = "error"
    INFO_MESSAGE = "info"


class SlackMesaageColorEnum(Enum):
    """
    Slack message color value according to status.
    """

    SUCCESS_MESSAGE_COLOR = "#28a745"
    ERROR_MESSAGE_COLOR = "#dc3545"
    INFO_MESSAGE_COLOR = "#17a2b8"


class SlackMesaageIconEnum(Enum):
    """
    Slack message Icon value according to status.
    """

    SUCCESS_MESSAGE_ICON = ":smile:"
    ERROR_MESSAGE_ICON = ":crycry2:"
    INFO_MESSAGE_ICON = ":bell:"
