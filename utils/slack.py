import json
import requests

from loguru import logger

from constants import SlackMesaageColorEnum, SlackMessageTypeEnum, SlackMesaageIconEnum


def _make_slack_message(slack_message_type: str, server_name: str, utilization: float) -> str:
    """
    Send slack message according to the state of the GPU utilization

    Args:
        status (str): status of GPU utilization
        server_name (str): name that identifies the server
        utilization (float): GPU utilization

    Returns:
        str: value for sending slack message(json format)
    """
    if slack_message_type == SlackMessageTypeEnum.SUCCESS_MESSAGE.value:
        fields = [
            {
                "title": "GPU utilization is normal",
                "value": f"GPU Server: {server_name}\nGPU Utilization: {utilization}",
                "short": False,
            },
        ]
        color = SlackMesaageColorEnum.SUCCESS_MESSAGE_COLOR.value
        icon = SlackMesaageIconEnum.SUCCESS_MESSAGE_ICON.value
    elif slack_message_type == SlackMessageTypeEnum.ERROR_MESSAGE.value:
        fields = [
            {
                "title": "GPU utilization is abnormal",
                "value": f"GPU Server: {server_name}\nGPU Utilization: {utilization}",
                "short": False,
            },
        ]
        color = SlackMesaageColorEnum.ERROR_MESSAGE_COLOR.value
        icon = SlackMesaageIconEnum.ERROR_MESSAGE_ICON.value
    elif slack_message_type == SlackMessageTypeEnum.INFO_MESSAGE.value:
        fields = [
            {
                "title": "GPU monitoring start",
                "value": f"GPU Server: {server_name}\nGPU Utilization: {utilization}",
                "short": False,
            },
        ]
        icon = SlackMesaageIconEnum.INFO_MESSAGE_ICON.value
    else:
        raise ValueError("Unexpected slack message type : ", slack_message_type)
    return json.dumps(
        {
            "attachments": [
                {
                    "color": color,
                    "fields": fields,
                }
            ],
            "icon_emoji": icon,
        }
    )


class SlackWebhookBot:
    """
    Send slack message
    """

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_message(self, status: str, server_name: str, utilization: float) -> dict:
        """
        Send slack message

        Args:
            status (str): status of GPU utilization
            server_name (str): name that identifies the server
            utilization (float): GPU utilization

        Returns:
            dict: status info of request
        """
        try:
            response = requests.post(
                url=self.webhook_url,
                headers={"Content-Type": "application/json; charset=utf-8"},
                json=_make_slack_message(status, server_name, utilization),
            )
            if response.status_code == 200:
                return {"is_error": False, "text": response.text}
            logger.error("Error occured while sending slack message : ", response.text)
            return {"is_error": True, "text": response.text}
        except Exception as error:
            logger.error("Unexpected error occurred while sending slack message : ", error)
            return {"is_error": True, "text": f"Unexpected error occurred: {error}"}
