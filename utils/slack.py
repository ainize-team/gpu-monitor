import requests

from loguru import logger

from constants import SlackMesaageColorEnum


def _make_message(status: str, server_name: str, utilization: float) -> dict:
    """
    Send slack message according to the state of the gpu utilization

    Args:
        status (str): status of gpu utilization
        server_name (str): name that identifies the server
        utilization (float): gpu utilization

    Returns:
        dict: value for sending slack message
    """
    if status == "success":
        text = ":thumbsup: GPU utilization is normal. :thumbsup:"
        fields = []
        color = SlackMesaageColorEnum.SUCCESS_MESSAGE_COLOR.value
    if status == "error":
        text = "*:exclamation: GPU utilization is abnormal. :exclamation:*"
        fields = [
            {"value": f"GPU Utilization: {utilization}", "short": False},
        ]
        color = SlackMesaageColorEnum.ERROR_MESSAGE_COLOR.value

    return {
        "color": color,
        "author_name": server_name,
        "text": text,
        "fields": fields,
    }


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
            status (str): status of gpu utilization
            server_name (str): name that identifies the server
            utilization (float):gpu utilization

        Returns:
            dict: status info of request
        """
        try:
            response = requests.post(
                url=self.webhook_url,
                headers={"Content-Type": "application/json; charset=utf-8"},
                json={"attachments": _make_message(status, server_name, utilization)},
            )
            if response.status_code == 200:
                return {"is_error": False, "text": response.text}
            logger.error("Error occured while sending slack message : ", response)
            return {"is_error": True, "text": response.text}
        except Exception as error:
            logger.error("Unexpected error occurred while sending slack message : ", error)
            return {"is_error": True, "text": f"Unexpected error occurred: {error}"}
