import requests
from typing import Dict, List

COLOR: Dict[str, str] = {
    "success": "#28a745",
    "warning": "#ffc107",
    "danger": "#dc3545",
}


def _make_message(
    status: str, server_name: str, first_occurrence_time: str, utilization: float
) -> List:
    if status == "success":
        text = ":thumbsup: GPU utilization has been restored to normal. :thumbsup:"
        fields = []
    else:
        if status == "warning":
            text = "*:question: GPU utilization is low. :question:*"
        else:
            text = "*:exclamation: GPU utilization has been low for a long time. :exclamation:*"
        fields = [
            {"value": f"First Occurrence Time: {first_occurrence_time}", "short": False},
            {"value": f"GPU Utilization: {utilization}", "short": False},
        ]
    return [{"color": COLOR[status], "author_name": server_name, "text": text, "fields": fields}]


class SlackWebhookBot:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_message(
        self, status: str, server_name: str, first_occurrence_time: str, utilization: float
    ) -> bool:
        try:
            response = requests.post(
                url=self.webhook_url,
                headers={"Content-Type": "application/json; charset=utf-8"},
                json={
                    "attachments": _make_message(
                        status, server_name, first_occurrence_time, utilization
                    )
                },
            )
            if response.status_code == 200:
                return {"error": False, "text": response.text}
            return {"error": True, "text": response.text}
        except Exception as e:
            return {"error": True, "text": f"Unexpected error occurred: {e}"}

    def send_error(self, server_name, message):
        try:
            response = requests.post(
                url=self.webhook_url,
                headers={"Content-Type": "application/json; charset=utf-8"},
                json={
                    "attachments": [
                        {
                            "color": COLOR["danger"],
                            "author_name": server_name,
                            "text": "Unexpected Error Occurs",
                            "fields": [{"value": f"{message}", "short": False}],
                        }
                    ]
                },
            )
            if response.status_code == 200:
                return {"error": False, "text": response.text}
            return {"error": True, "text": response.text}
        except Exception as e:
            return {"error": True, "text": f"Unexpected error occurred: {e}"}
